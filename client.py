import sys
import time
import json
from socket import *


def outgoing_message():
    msg = {'action': 'presence', 'time': time.time()}
    return json.dumps(msg).encode('utf-8')


def incoming_message(msg):
    dct = json.loads(msg.decode('utf-8'))
    print(dct)


def main():
    try:
        addr = sys.argv[1]
        port = int(sys.argv[2])
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        print('номер порта вне диапазона (1024, 65535)')
        sys.exit(1)
    except IndexError:
        print('Необходимо указать адрес и порт сервера')
        sys.exit(1)
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((addr, port))
    s.send(outgoing_message())
    msg = s.recv(1024)
    incoming_message(msg)
    s.close()


if __name__ == '__main__':
    main()
