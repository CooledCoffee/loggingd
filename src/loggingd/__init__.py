# -*- coding: UTF-8 -*-
from decorated import Function
from logging import getLogger, DEBUG, INFO, WARN, ERROR, CRITICAL
from loggingd import util
from loggingd.decorators import log_enter, log_return, log_error
from loggingd.util import disable_module_log
import logging

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
    disable_module_log(Function.__module__) #@UndefinedVariable
    disable_module_log('loggingd.decorators')
    