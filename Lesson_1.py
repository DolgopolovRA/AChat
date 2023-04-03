import subprocess
import chardet
from chardet.universaldetector import UniversalDetector

# Задание №1

print('=====Задание №1=====')
s1, s2, s3 = 'разработка', 'сокет', 'декоратор'
s1U, s2U, s3U = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', '\u0441\u043e\u043a\u0435\u0442', \
                '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
print(f'{type(s1), s1}\n{type(s2), s2}\n{type(s3), s3}\n{type(s1U), s1U}\n{type(s2U), s2U}\n{type(s3U), s3U}\n')


# Задание №2

print('=====Задание №2=====')
var1, var2, var3 = b'class', b'function', b'method'
print(f'тип - {type(var1)} содержимое - {var1} длина - {len(var1)}')
print(f'тип - {type(var2)} содержимое - {var2} длина - {len(var2)}')
print(f'тип - {type(var3)} содержимое - {var3} длина - {len(var3)}')
print()

# Задание №3

print('=====Задание №3=====')
lst = ('attribute', 'класс', 'функция', 'type')

for el in lst:
    try:
        print(bytes(el, 'ascii'))
    except ValueError:
        print(f'слово "{el}" невозможно записать в байтовом типе')

print()

# Задание №4

print('=====Задание №4=====')

lst = ('разработка', 'администрирование', 'protocol', 'standard')

lst_encode = [el.encode('utf-8') for el in lst]
print(lst_encode)

lst_decode = [el.decode() for el in lst_encode]
print(lst_decode)

print()

# Задание №5

print('=====Задание №5=====')

args = ['ping', 'yandex.ru']

subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for el in subproc_ping.stdout:
    print(el.decode('cp866'))

print()

# Задание №6

print('=====Задание №6=====')

# определяем кодировку файла
detector = UniversalDetector()
with open('test_file.txt', 'rb') as file:
    for line in file.readlines():
        detector.feed(line)
        if detector.done:
            break

detector.close()
codes = detector.result['encoding']
print(f'кодировка файла {codes}')
print()
# открываем файл в правильной кодировке
with open( 'test_file.txt', 'r', encoding=codes) as file:
    for line in file.readlines():
        print(line, end='')
