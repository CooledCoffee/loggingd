# -*- coding: utf-8 -*-
from collections import defaultdict
from logging import LogRecord, Logger

import six
from decorated.base.context import ContextMeta


class LoggingSession(six.with_metaclass(ContextMeta)):
    def __init__(self, **fields):
        self.fields = fields

def patch():
    original_log = Logger._log
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        session = LoggingSession.current()
        if session is not None:
            extra = extra or {}
            extra.update(session.fields)
        if stack_info:
            # for python3
            return original_log(self, level, msg, args, exc_info=exc_info, extra=extra, stack_info=True)
        else:
            # for python2 & python3 without stack_info
            return original_log(self, level, msg, args, exc_info=exc_info, extra=extra)
    Logger._log = _log

    def _makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        if sinfo is not None:
            # for python3
            rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo)
        else:
            # for python2 & python3 without sinfo
            rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func)
        if extra is not None:
            rv.__dict__.update(extra)
        rv.__dict__ = defaultdict(str, rv.__dict__)
        return rv
    Logger.makeRecord = _makeRecord
