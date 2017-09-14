# -*- coding: utf-8 -*-
from logging import LogRecord, Logger

import six
from decorated.base.context import ContextMeta


class LoggingSession(six.with_metaclass(ContextMeta)):
    def __init__(self, **fields):
        self.fields = fields

def patch():
    original_log = Logger._log
    def _log(self, level, msg, args, exc_info=None, extra=None):
        session = LoggingSession.current()
        if session is not None:
            extra = extra or {}
            extra.update(session.fields)
        return original_log(self, level, msg, args, exc_info=exc_info, extra=extra)
    Logger._log = _log

    def _makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func)
        if extra is not None:
            rv.__dict__.update(extra)
        return rv
    Logger.makeRecord = _makeRecord
