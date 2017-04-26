# -*- coding: utf-8 -*-
import logging
from logging import Filter

import six
from decorated.base.context import ContextMeta


class LoggingSession(six.with_metaclass(ContextMeta)):
    def __init__(self, **fields):
        self.fields = fields

class SessionFilter(Filter):
    def filter(self, record):
        session = LoggingSession.current()
        if session is not None:
            for k, v in session.fields.items():
                setattr(record, k, v)
        return True

def patch():
    filter = SessionFilter()
    logging.getLogger().addFilter(filter)
