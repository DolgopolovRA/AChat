import sys
import time
import json
from socket import *
import logging
import log.client_log_config
import inspect


lg = logging.getLogger('client')


def _log(func):
    def wrapper(*args, **kwargs):
        lg.info(f'Вызов функции {func.__name__} с аргументами {args, kwargs}')
        lg.info(f'Функция {func.__name__}() вызвана из функции {inspect.stack()[1][3]}')
        return func(*args, **kwargs)
    return wrapper


@_log
def outgoing_message():
    msg = {'action': 'presence', 'time': time.time()}
    return json.dumps(msg).encode('utf-8')


@_log
def incoming_message(msg):
    dct = json.loads(msg.decode('utf-8'))
    return dct


def main():
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
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((addr, port))
    s.send(outgoing_message())
    msg = s.recv(1024)
    print(incoming_message(msg))
    s.close()


if __name__ == '__main__':
    main()
