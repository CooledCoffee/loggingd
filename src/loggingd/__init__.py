# -*- coding: UTF-8 -*-
from decorated import Function
from loggingd import util
from loggingd.decorators import log_enter, log_return, log_error
import logging

def init(level=logging.INFO):
    logging.getLogger().setLevel(level)
    util.patch_logging()
    util.disable_module_log(Function.__module__) #@UndefinedVariable
    util.disable_module_log('loggingd.decorators')
    