import sys
from socket import *
import json
import time
import logging
import log.server_log_config
from utils import get_func_name

lg = logging.getLogger('server')


class PortError(Exception):
    def __str__(self):
        return 'Не указан номер порта'


class AddrError(Exception):
    def __str__(self):
        return 'Не указан адрес, который будет слушать сервер'


def incoming_message(msg):
    lg.info(f'Выполнена функция {get_func_name()} модуля {sys.argv[0]}')
    msg_from_client = json.loads(msg.decode('utf-8'))
    if type(msg_from_client) is dict:
        if msg_from_client.get('action') == 'presence' and msg_from_client.get('time'):
            return msg_from_client, {'responce': 200, 'time': time.time()}
    return '', {'responce': 400, 'time': time.time()}


def outgoing_message(answer):
    lg.info(f'Выполнена функция {get_func_name()} модуля {sys.argv[0]}')
    return json.dumps(answer).encode('utf-8')


def main():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
            if port < 1024 or port > 65535:
                raise ValueError
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

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)

    while True:
        client, addr = s.accept()
        msg = client.recv(1024)
        msg_from_client, status = incoming_message(msg)
        if msg_from_client:
            print(msg_from_client)
        client.send(outgoing_message(status))
        client.close()


if __name__ == '__main__':
    main()
