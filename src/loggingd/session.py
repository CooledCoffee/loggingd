# -*- coding: utf-8 -*-
import six
from decorated.base.context import ContextMeta


class LoggingSession(six.with_metaclass(ContextMeta)):
    def __init__(self, **fields):
        self.fields = fields
