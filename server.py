import inspect
import select
import sys
from socket import *
import json
import time
import logging
import log.server_log_config
from utils import get_func_name

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


@_log
def incoming_message(msg):
    msg_from_client = json.loads(msg.decode('utf-8'))
    #if type(msg_from_client) is dict:
     #   if msg_from_client.get('action') == 'presence' and msg_from_client.get('time'):
      #      return msg_from_client, {'responce': 200, 'time': time.time()}
    return msg_from_client


@_log
def outgoing_message(answer):
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

    clients = []
    request = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    s.settimeout(0.3)
    while True:
        try:
            client, addr = s.accept()
        except OSError:
            pass
        else:
            print(f'Получен запрос от {addr}')
            clients.append(client)
        finally:
            read_client = []
            write_client = []
            try:
                read_client, write_client, er = select.select(clients, clients, clients, 5)
            except:
                pass
            for conn in read_client:
                try:
                    msg = conn.recv(1024)
                    msg_from_client = incoming_message(msg)
                    write_client.remove(conn)
                except:
                    clients.remove(conn)
                else:
                    if msg_from_client:
                        print(f'Получено сообщение {msg_from_client}')
                        request.append(msg_from_client)
            for el in request:
                for conn in write_client:
                    try:
                        conn.send(outgoing_message(el))
                    except:
                        pass
                    finally:
                        pass
            request.clear()


if __name__ == '__main__':
    main()
