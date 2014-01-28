# -*- coding: UTF-8 -*-
from decorated.base import function
from decorated.decorators import events
from loggingd import util
from loggingd.decorators import log_enter, log_return, log_error, log_exit
from loggingd.util import disable_module_log
import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
getLogger = logging.getLogger

disable_module_log = disable_module_log
log_enter = log_enter
log_error = log_error
log_exit = log_exit
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
    