# -*- coding: utf-8 -*-
from collections import defaultdict
from logging import Formatter

import six
import sys
from decorated.base.context import ContextMeta


class LoggingSession(six.with_metaclass(ContextMeta)):
    def __init__(self, **fields):
        self.fields = fields

class LoggingdFormatter(Formatter):
    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        try:
            d = defaultdict(str, **record.__dict__)
            session = LoggingSession.current()
            if session is not None:
                d.update(session.fields)
            s = self._fmt % d
        except UnicodeDecodeError as e:
            # Issue 25664. The logger name may be Unicode. Try again ...
            try:
                record.name = record.name.decode('utf-8')
                s = self._fmt % record.__dict__
            except UnicodeDecodeError:
                raise e
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                s = s + record.exc_text.decode(sys.getfilesystemencoding(),
                                               'replace')
        return s
