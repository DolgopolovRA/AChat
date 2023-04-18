import logging

format_ = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

fl = logging.FileHandler('log/client.log', encoding='utf-8')
fl.setFormatter(format_)

client_logger = logging.getLogger('client')
client_logger.addHandler(fl)
client_logger.setLevel(logging.INFO)
