from os import path
from logging.config import fileConfig
from logging import getLogger

log_file_path = path.join(path.dirname(path.abspath(__file__)), '..', 'logging_config.ini')
fileConfig(log_file_path, disable_existing_loggers = False)


__version__ = '1.0.2'
