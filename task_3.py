import yaml

dct = {'\u0410': ['1', '2', '3'], '\u0411': 123, '\u0414': {'dict1': {'F': '2221'}}}
with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(dct, f, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as f:
    print(yaml.load(f, Loader=yaml.FullLoader))
