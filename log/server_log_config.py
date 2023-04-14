import logging
from logging.handlers import TimedRotatingFileHandler

format_ = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

rt = TimedRotatingFileHandler('log/server.log', when='D', interval=1, encoding='utf-8')
rt.setFormatter(format_)

server_logger = logging.getLogger('server')
server_logger.addHandler(rt)
server_logger.setLevel(logging.INFO)
