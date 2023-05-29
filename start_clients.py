import subprocess
import sys


if __name__ == '__main__':
    try:
        i = int(sys.argv[1])
    except:
        i = 2

    for _ in range(i):
        res = subprocess.Popen(['python', 'client.py', 'localhost', '5555'], creationflags=subprocess.CREATE_NEW_CONSOLE)

