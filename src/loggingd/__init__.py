# -*- coding: UTF-8 -*-
from logging import NOTSET, DEBUG, INFO, WARN, ERROR, CRITICAL, getLogger, Logger
from loggingd import config
from loggingd.config import DEFAULT_FORMAT, add_console_handler, add_file_handler, init, yaml_config
from loggingd.decorators import LogAndIgnoreError, LogEnter, LogError, LogReturn
from loggingd.session import LoggingSession

log_enter = LogEnter # pylint: disable=invalid-name
log_return = LogReturn # pylint: disable=invalid-name
log_error = LogError # pylint: disable=invalid-name
log_and_ignore_error = LogAndIgnoreError # pylint: disable=invalid-name

def _patch():
    original_log = Logger._log
    def _log(self, level, msg, args, exc_info=None, extra=None):
        session = LoggingSession.current()
        if session is not None:
            extra = extra or {}
            extra.update(session.fields)
        return original_log(self, level, msg, args, exc_info=exc_info, extra=extra)
    Logger._log = _log
_patch()
