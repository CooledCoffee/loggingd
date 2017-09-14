# -*- coding: UTF-8 -*-
from logging import NOTSET, DEBUG, INFO, WARN, ERROR, CRITICAL, getLogger, Logger
from loggingd import config
from loggingd.config import DEFAULT_FORMAT, add_console_handler, add_file_handler, init, yaml_config
from loggingd.decorators import LogAndIgnoreError, LogEnter, LogError, LogReturn
from loggingd import util
from loggingd.util import LoggingSession

log_enter = LogEnter # pylint: disable=invalid-name
log_return = LogReturn # pylint: disable=invalid-name
log_error = LogError # pylint: disable=invalid-name
log_and_ignore_error = LogAndIgnoreError # pylint: disable=invalid-name


util.patch()
