import logging
from logging.handlers import RotatingFileHandler
from settings import LOG_FILE

logging.basicConfig(
        handlers=[logging.StreamHandler(),
                  RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=10)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(pathname)s -> %(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
my_log = logging.getLogger()
