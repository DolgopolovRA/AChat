import re
import csv


def get_data():
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    s = {}
    for i in range(1, 4):
        with open(f'info_{i}.txt', 'r') as f:
            res = re.findall(r'Изготовитель системы:\s+.+\n|Название ОС:\s+.+\n|Код продукта:\s+.+\n|'
                             r'Тип системы:\s+.+\n', f.read())
        for el in res:
            lst = el.split(':')
            s[lst[0]] = lst[1].strip()
        os_prod_list.append(s.get("Изготовитель системы"))
        os_name_list.append(s.get('Название ОС'))
        os_code_list.append(s.get('Код продукта'))
        os_type_list.append(s.get('Тип системы'))
        main_data.append([os_prod_list[i-1], os_name_list[i-1], os_code_list[i-1], os_type_list[i-1]])

    return main_data


def write_to_csv(path):
    data = get_data()
    with open(path, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        f_writer.writerows(data)


write_to_csv('1.csv')
