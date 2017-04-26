# -*- coding: UTF-8 -*-
DEFAULT_FORMAT = '[%(asctime)s] [%(levelname)s] [%(process)d:%(threadName)s] [%(name)s:%(funcName)s:%(lineno)d]\n%(message)s'

from logging import NOTSET, DEBUG, INFO, WARN, ERROR, CRITICAL, getLogger
from loggingd import config
from loggingd.decorators import LogEnter, LogError, LogReturn, LogAndIgnoreError
from loggingd.config import init, yaml_config, add_console_handler, add_file_handler
from loggingd.session import LoggingSession

log_enter = LogEnter
log_return = LogReturn
log_error = LogError
log_and_ignore_error = LogAndIgnoreError
