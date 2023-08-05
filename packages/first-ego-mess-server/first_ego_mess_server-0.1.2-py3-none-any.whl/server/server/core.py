import threading
import logging
import select
import json
import hmac
import binascii
import os
import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

sys.path.append('../')
from common.descriptor import Port
from common.utils import send_message, get_message
from common.decorators import login_required
from common.variables import (ACCOUNT_NAME, ACTION, ADD_CONTACT, CONNECTION_TIMEOUT, DATA, DESTINATION, ERROR, EXIT,
                              GET_CONTACTS, LIST_INFO, MAX_CONNECTIONS, MESSAGE, MESSAGE_TEXT, PRESENCE, PUBLIC_KEY,
                              PUBLIC_KEY_REQUEST, REMOVE_CONTACT, RESPONSE, RESPONSE_200, RESPONSE_202, RESPONSE_205,
                              RESPONSE_400, RESPONSE_511, SENDER, TIME, USER, USERS_REQUEST)

LOGGER = logging.getLogger('server')


class MessageProcessor(threading.Thread):
    """
    The main server class. Accepts connections, dictionaries (packets from clients),
    processes incoming messages. Runs as a separate thread.
    """

    port = Port()

    def __init__(self, listen_addr, listen_port, database):
        self.addr = listen_addr
        self.port = listen_port
        self.database = database

        self.clients = []
        self.names = dict()

        # Сокеты
        self.sock = None
        self.listen_sockets = None
        self.error_sockets = None

        # Флаг продолжения работы
        self.running = True

        super().__init__()

    def run(self):
        """The method that the main thread loop."""

        self.init_socket()

        while self.running:
            try:
                client, client_addr = self.sock.accept()
            except OSError:
                pass
            else:
                LOGGER.info(f'Connection established: {client_addr}')
                client.settimeout(5)
                self.clients.append(client)

            recv_list = []
            send_list = []
            err_list = []

            try:
                if self.clients:
                    recv_list, self.listen_sockets, self.error_sockets = select.select(
                        self.clients, self.clients, [], 0
                    )
            except OSError as err:
                LOGGER.error(f'Sockets error: {err.errno}')

            if recv_list:
                for client_with_message in recv_list:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        LOGGER.debug('Getting data from client exception.', exc_info=err)
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        """
        The client handler method with which the connection interrupted.
        Looks for a client and removes him from the lists and database.
        """

        LOGGER.info(f'{client.getpeername()} disconnected from the server.')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def init_socket(self):
        """The method that initializes the socket."""

        LOGGER.info(
            f'Server started, connection port: {self.port}; address from which connections are accepted: {self.addr}. '
            f'If the address is not specified, connections from any address are accepted.'
        )

        transport = socket(AF_INET, SOCK_STREAM)
        transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        transport.bind((self.addr, self.port))
        transport.settimeout(CONNECTION_TIMEOUT)

        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def process_message(self, message):
        """Method for sending a message to the client."""

        if message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] in self.listen_sockets:
            try:
                send_message(self.names[message[DESTINATION]], message)
                LOGGER.info(f'Sent a message to {message[DESTINATION]} from {message[SENDER]}')
            except OSError:
                self.remove_client(message[DESTINATION])
        elif message[DESTINATION] in self.names \
                and self.names[message[DESTINATION]] not in self.listen_sockets:
            LOGGER.error(
                f'Communication with the client {message[DESTINATION]} was lost. Connection closed, no delivery possible'
            )
            self.remove_client(self.names[message[DESTINATION]])
        else:
            LOGGER.error(
                f'User {message[DESTINATION]} is not registered on the server, sending a message is not possible'
            )

    @login_required
    def process_client_message(self, message, client):
        """Incoming message handler method."""

        LOGGER.debug(f'Parsing a message from a client: {message}')

        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message \
                and message[ACTION] == PRESENCE \
                and TIME in message \
                and USER in message:
            # Если сообщение о присутствии, то вызываем функцию авторизации
            self.authorize_user(message, client)

        # Если это сообщение, то отправляем его получателю
        elif ACTION in message \
                and message[ACTION] == MESSAGE \
                and DESTINATION in message \
                and TIME in message \
                and SENDER in message \
                and MESSAGE_TEXT in message \
                and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.database.process_message(message[SENDER], message[DESTINATION])
                self.process_message(message)
                try:
                    send_message(client, RESPONSE_200)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'The user is not registered on the server'
                try:
                    send_message(client, response)
                except OSError:
                    pass
            return

        # Если клиент выходит
        elif ACTION in message \
                and message[ACTION] == EXIT \
                and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.remove_client(client)

        # Если это запрос контакт-листа
        elif ACTION in message \
                and message[ACTION] == GET_CONTACTS \
                and USER in message \
                and self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # Если это добавление контакта
        elif ACTION in message \
                and message[ACTION] == ADD_CONTACT \
                and ACCOUNT_NAME in message \
                and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это удаление контакта
        elif ACTION in message \
                and message[ACTION] == REMOVE_CONTACT \
                and ACCOUNT_NAME in message \
                and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это запрос известных пользователей
        elif ACTION in message \
                and message[ACTION] == USERS_REQUEST \
                and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0] for user in self.database.users_list()]
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # Если это запрос публичного ключа пользователя
        elif ACTION in message \
                and message[ACTION] == PUBLIC_KEY_REQUEST \
                and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_public_key(message[ACCOUNT_NAME])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'No public key for this user'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)

        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'The request is invalid'
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

    def authorize_user(self, message, sock):
        """The method that implements user authorization."""

        LOGGER.debug(f'Start auth process for {message[USER]}')

        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Username already taken'
            try:
                LOGGER.debug(f'Username busy, sending {response}')
                send_message(sock, response)
            except OSError:
                LOGGER.debug('OS Error')
                pass
            self.clients.remove(sock)
            sock.close()

        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = RESPONSE_400
            response[ERROR] = 'User not registered'
            try:
                LOGGER.debug(f'Unknown username, sending {response}')
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            LOGGER.debug('Correct username, starting password check')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем серверную версию ключа
            hash = hmac.new(self.database.get_hash(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = hash.digest()
            LOGGER.debug(f'Auth message: {message_auth}')
            try:
                # Обмен с клиентом
                send_message(sock, message_auth)
                answer = get_message(sock)
            except OSError as err:
                LOGGER.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(answer[DATA])
            # Если ответ клиента корректный, то сохраняем его в список пользователей
            if RESPONSE in answer \
                    and answer[RESPONSE] == 511 \
                    and hmac.compare_digest(digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()

                try:
                    send_message(sock, RESPONSE_200)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])

                # добавляем пользователя в список активных и,
                # если у него изменился открытый ключ, то сохраняем новый
                self.database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY]
                )

            else:
                response = RESPONSE_400
                response[ERROR] = 'Invalid password'

                try:
                    send_message(sock, response)
                except OSError:
                    pass

                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        """Method that implements sending service message 205 to clients."""

        for client in self.names:
            try:
                send_message(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])
