import sys
import time
import json
from socket import *
import logging
import log.client_log_config
import inspect
from threading import Thread, Lock
from metaclass import ClientVerifier
from time import sleep
from database import ClientDb


lg = logging.getLogger('client')


def _log(func):
    def wrapper(*args, **kwargs):
        lg.info(f'Вызов функции {func.__name__} с аргументами {args, kwargs}')
        lg.info(f'Функция {func.__name__}() вызвана из функции {inspect.stack()[1][3]}')
        return func(*args, **kwargs)
    return wrapper


def cln_params():
    try:
        addr = sys.argv[1]
        port = int(sys.argv[2])
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        lg.exception('номер порта вне диапазона (1024, 65535)')
        sys.exit(1)
    except IndexError:
        lg.exception('Необходимо указать адрес и порт сервера')
        sys.exit(1)
    return addr, port


class Client(metaclass=ClientVerifier):

    def __init__(self, addr, port, s, login, db):
        self.s = s
        self.addr = addr
        self.port = port
        self.login = login
        self.db = db

    @_log
    def outgoing_message(self, msg):
        return json.dumps(msg).encode('utf-8')

    @_log
    def incoming_message(self, msg):
        dct = json.loads(msg.decode('utf-8'))
        return dct

    def send_msg(self, sock, init=True):
        while True:
            if init:
                sock.send(self.outgoing_message({'action': 'presence', 'addr': self.addr, 'login': self.login}))
                sleep(1)
                sock.send(self.outgoing_message({"action": "get_contacts", "time": time.time(), "user_login": self.login}))
                init = False
            else:
                msg = input()
                if msg == 'contact_list':
                    sock.send(self.outgoing_message({"action": "get_contacts", "time": time.time(), "user_login": self.login}))
                else:
                    sock.send(self.outgoing_message(f'{self.login}:{msg}'))

    def read_msg(self, sock):
        while True:
            msg = sock.recv(1024)
            msg = self.incoming_message(msg)
            if type(msg) is dict:
                if msg.get('response') == '202':
                    sp = msg.get('alert')
                    self.db.init_contacts_list(sp, self.login)
            else:
                print(msg)
                self.db.add_to_message_history(msg)

    def cln_main(self):

        t1 = Thread(target=self.send_msg, args=(self.s,))
        t1.daemon = True
        t1.start()
        t2 = Thread(target=self.read_msg, args=(self.s,))
        t2.daemon = True
        t2.start()
        t1.join()
        t2.join()


def main():
    db = ClientDb()
    login = input('Введите логин: ')
    addr, port = cln_params()
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((addr, port))
    cl = Client(addr, port, s, login, db)
    cl.cln_main()


if __name__ == '__main__':
    main()
