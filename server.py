import inspect
import select
import sys
from socket import *
import json
import time
import logging
from typing import List, Any

import log.server_log_config
from utils import get_func_name
from metaclass import ServerVerifier
from database import ServerDb

lg = logging.getLogger('server')


def _log(func):
    def wrapper(*args, **kwargs):
        lg.info(f'Вызов функции {func.__name__} с аргументами {args, kwargs}')
        lg.info(f'Функция {func.__name__}() вызвана из функции {inspect.stack()[1][3]}')
        return func(*args, **kwargs)

    return wrapper


class PortError(Exception):
    def __str__(self):
        return 'Не указан номер порта'


class AddrError(Exception):
    def __str__(self):
        return 'Не указан адрес, который будет слушать сервер'


class Port:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if value < 1024 or value > 65535 or type(value) != int:
            raise PortError
        instance.__dict__[self.name] = value


def srv_params():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            raise PortError
        if '-a' in sys.argv:
            addr = sys.argv[sys.argv.index('-a') + 1]
        else:
            raise AddrError
    except PortError as pe:
        lg.exception(pe)
        sys.exit(1)
    except AddrError as ae:
        lg.exception(ae)
        sys.exit(1)
    except ValueError:
        lg.exception('номер порта вне диапазона (1024, 65535)')
        sys.exit(1)
    except IndexError:
        lg.exception('после параметров "-p" и "-a" должны быть указаны значения')
        sys.exit(1)
    return addr, port


class Server(metaclass=ServerVerifier):
    port = Port()

    def __init__(self, addr, l_port, db):
        self.s = None
        self.port = l_port
        self.addr = addr
        self.clients = []
        self.request = []
        self.db = db
        self.online_clients_socket = {}

    def init_sock(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.addr, self.port))
        self.s = s
        self.s.listen(5)
        self.s.settimeout(0.3)

    @_log
    def incoming_message(self, msg):
        msg_from_client = json.loads(msg.decode('utf-8'))
        return msg_from_client

    @_log
    def outgoing_message(self, answer):
        return json.dumps(answer).encode('utf-8')

    def srv_main(self):

        self.init_sock()

        while True:
            try:
                client, addr = self.s.accept()
            except OSError:
                pass
            else:
                print(f'Получен запрос от {addr} в {time.time()}')
                self.clients.append(client)
                self.online_clients_socket[client] = ''
            finally:
                read_client = []
                write_client = []
                try:
                    read_client, write_client, er = select.select(self.clients, self.clients, self.clients, 5)
                except:
                    pass
                for conn in read_client:
                    try:
                        msg = conn.recv(1024)
                        msg_from_client = self.incoming_message(msg)
                        write_client.remove(conn)
                    except:
                        self. clients.remove(conn)
                        login_del = self.online_clients_socket.pop(conn, None)
                        if login_del:
                            self.db.del_active_users(login_del)
                    else:
                        if msg_from_client:
                            print(f'Получено сообщение {msg_from_client}')
                            if type(msg_from_client) is dict:
                                if msg_from_client.get('login') in self.online_clients_socket.values():
                                    conn.send(self.outgoing_message('Пользователь с таким именем уже есть в системе!'))
                                    self.clients.remove(conn)
                                    self.online_clients_socket.pop(conn)
                                    self.db.del_active_users(msg_from_client.get('login'))
                                    conn.close()
                                elif msg_from_client.get('action') == 'get_contacts':
                                    conn.send(self.outgoing_message({'response': '202', 'alert': f'{list(self.online_clients_socket.values())}'}))
                                else:
                                    self.db.login(msg_from_client.get('login'), msg_from_client.get('addr'))
                                    self.online_clients_socket[conn] = msg_from_client.get('login')
                                    # conn.send(self.outgoing_message('Подключение к серверу выполнено успешно!'))
                            else:
                                self.request.append(msg_from_client)
                for el in self.request:
                    for conn in write_client:
                        try:
                            conn.send(self.outgoing_message(el))
                        except:
                            pass
                        finally:
                            pass
                self.request.clear()


def main():
    db = ServerDb()
    addr, port = srv_params()
    srv = Server(addr, port, db)
    srv.srv_main()


if __name__ == '__main__':
    main()
