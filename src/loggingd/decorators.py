# -*- coding: UTF-8 -*-
import logging
import re

from decorated import WrapperFunction
from decorated.base.expression import Expression
from decorated.base.template import Template


class Log(WrapperFunction):
    level = logging.INFO

    def _decorate(self, func):
        super(Log, self)._decorate(func)
        self._logger = self._logger or logging.getLogger(self.__module__)
        return self
    
    def _evaluate_expressions(self, ret, e, *args, **kw):
        arg_dict = self._resolve_args(*args, **kw)
        arg_dict['ret'] = ret
        arg_dict['e'] = e
        try:
            condition = self._condition(**arg_dict)
        except Exception:
            self._logger.warn('Failed to evaluate logging condition.', exc_info=True)
            condition = True
        if condition:
            return True, self._msg(**arg_dict)
        else:
            return False, None
    
    def _init(self, message, condition=Expression('True'), logger=None, **kw): # pylint: disable=arguments-differ
        super(Log, self)._init()
        self._level, self._msg = _parse_expression(message, self.level)
        self._msg = Template(self._msg)
        self._condition = condition if callable(condition) else Expression(condition)
        self._logger = logger
        self._extra_kw = kw

    def _log(self, ret, e, *args, **kw):
        condition, msg = self._evaluate_expressions(ret, e, *args, **kw)
        if condition:
            extra = kw.get('extra', {})
            extra['lineno'] = self._func.__code__.co_firstlineno
            self._logger.log(self._level, msg, exc_info=self._extra_kw.get('exc_info'), extra=extra)
                
class LogEnter(Log):
    def _before(self, *args, **kw):
        self._log(None, None, *args, **kw)
    
class LogReturn(Log):
    def _after(self, ret, *args, **kw):
        self._log(ret, None, *args, **kw)
    
class LogError(Log):
    level = logging.WARN
    
    def _error(self, error, *args, **kw):
        self._log(None, error, *args, **kw)
    
class LogAndIgnoreError(Log):
    level = logging.WARN

    def _init(self, *args, **kw): # pylint: disable=arguments-differ
        self._error_classes = kw.pop('error_classes', Exception)
        super(LogAndIgnoreError, self)._init(*args, **kw)

    def _call(self, *args, **kw):
        try:
            return super(LogAndIgnoreError, self)._call(*args, **kw)
        except Exception as e:
            if isinstance(e, self._error_classes):
                self._log(None, e, *args, **kw)
            else:
                raise
    
_LEVEL_MAPPING = {
    'DEBUG' : logging.DEBUG,
    'INFO' : logging.INFO,
    'WARN' : logging.WARN,
    'ERROR' : logging.ERROR,
    'CRITICAL' : logging.CRITICAL,
    'D' : logging.DEBUG,
    'I' : logging.INFO,
    'W' : logging.WARN,
    'E' : logging.ERROR,
    'C' : logging.CRITICAL,
}
_MESSAGE_TEMPLATE = re.compile('\\[(\\w+)\\] (.*)')
def _parse_expression(message, default_level):
    '''
    >>> _parse_expression('aaa', logging.INFO)
    (20, 'aaa')
    >>> _parse_expression('[WARN] aaa', logging.INFO)
    (30, 'aaa')
    >>> _parse_expression('[W] aaa', logging.INFO)
    (30, 'aaa')
    >>> _parse_expression('[UNKNOWN] aaa', logging.INFO)
    (30, 'aaa')
    '''
    match = _MESSAGE_TEMPLATE.match(message)
    if not match:
        return default_level, message
    
    level, msg = match.groups()
    level = _LEVEL_MAPPING.get(level.upper(), logging.WARN)
    return level, msg
    