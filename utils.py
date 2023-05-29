import traceback
import os
import ipaddress
import subprocess
from tabulate import tabulate


def get_func_name():
    stack = traceback.extract_stack()
    return stack[-2][2]


def host_ping(ip_lst):
    dct_ip = {'available': [], 'unavailable': []}
    print('Опрос диапазона...')
    for ip in ip_lst:
        with subprocess.Popen(f'ping -n 1 {ip}', stdout=subprocess.PIPE) as proc:
            resp = proc.stdout.read().decode('866')
        if 'Заданный узел недоступен' in resp or 'Превышен интервал' in resp:
            dct_ip['unavailable'].append(ip)
        #     print(f'Узел {ip} недоступен')
        else:
            dct_ip['available'].append(ip)
        #     print(f'Узел {ip} доступен')
    return dct_ip


def host_range_ping(rng, end=255):
    ip1, ip2, ip3, ip4 = rng.split('.')
    lst = [f'{ip1}.{ip2}.{ip3}.{i}' for i in range(int(ip4), end+1)]
    return host_ping(lst)


def host_range_ping_tab(rng, end=255):
    dct_ip = host_range_ping(rng, end)
    print(tabulate(dct_ip, headers='keys', tablefmt='grid'))


iplist = ['192.168.0.21', '192.168.1.100', '192.168.0.50', 'localhost']


if __name__ == '__main__':

    # host_ping(iplist)
    # host_range_ping('192.168.0.100', end=120)
    host_range_ping_tab('192.168.0.100', end=120)
