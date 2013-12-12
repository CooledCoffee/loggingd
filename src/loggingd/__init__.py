# -*- coding: UTF-8 -*-
from decorated.base import function
from decorated.decorators import events
from logging import getLogger, DEBUG, INFO, WARN, ERROR, CRITICAL
from loggingd import util
from loggingd.decorators import log_enter, log_return, log_error
from loggingd.util import disable_module_log
import logging

DEBUG = DEBUG
INFO = INFO
WARN = WARN
ERROR = ERROR
CRITICAL = CRITICAL

disable_module_log = disable_module_log
getLogger = getLogger
log_enter = log_enter
log_error = log_error
log_return = log_return

def add_console_handler(level, fmt='%(message)s'):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt))
    getLogger().addHandler(handler)
    
def add_file_handler(level, path, fmt='[%(asctime)s] [%(levelname)s] [%(process)d:%(threadName)s] [%(name)s:%(funcName)s:%(lineno)d]\n%(message)s'):
    logger = getLogger()
    handler = logging.FileHandler(path)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    
def init(level=logging.INFO):
    logging.getLogger().setLevel(level)
    util.patch_logging()
    disable_module_log(function.__name__)
    disable_module_log(events.__name__)
    disable_module_log('loggingd.decorators')
    