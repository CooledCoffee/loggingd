# -*- coding: UTF-8 -*-
from decorated import Function
from logging import getLogger, DEBUG, INFO, WARN, ERROR, CRITICAL
from loggingd import util
from loggingd.decorators import log_enter, log_return, log_error
from loggingd.util import disable_module_log
import logging

def init(level=logging.INFO):
    logging.getLogger().setLevel(level)
    util.patch_logging()
    disable_module_log(Function.__module__) #@UndefinedVariable
    disable_module_log('loggingd.decorators')
    