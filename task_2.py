import json


def write_order_to_json(item, quantity, price, buyer, date):
    dct = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(dct, f, indent=4)


write_order_to_json('Яблоко', '12', '45', 'Иванов И.И.', '04.04.2023')
