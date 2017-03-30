# -*- coding: UTF-8 -*-
DEFAULT_FORMAT = '[%(asctime)s] [%(levelname)s] [%(process)d:%(threadName)s] [%(name)s:%(funcName)s:%(lineno)d]\n%(message)s'

import logging

from loggingd import util
from loggingd.decorators import LogEnter, LogError, LogReturn, LogAndIgnoreError

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
getLogger = logging.getLogger

log_enter = LogEnter
log_return = LogReturn
log_error = LogError
log_and_ignore_error = LogAndIgnoreError

add_console_handler = util.add_console_handler
add_file_handler = util.add_file_handler
init = util.init
yaml_config = util.yaml_config
