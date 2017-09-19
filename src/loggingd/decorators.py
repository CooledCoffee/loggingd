# -*- coding: UTF-8 -*-
from decorated import WrapperFunction
import doctest
import logging
import re

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
            condition = eval(self._condition, arg_dict) # pylint: disable=eval-used
        except Exception:
            return True, 'Invalid condition: %s.' % self._condition
        if condition:
            return True, _evaluate_message(self._msg, arg_dict)
        else:
            return False, None
    
    def _init(self, expression, condition='True', logger=None, **kw): # pylint: disable=arguments-differ
        super(Log, self)._init()
        self._level, self._msg = _parse_expression(expression, self.level)
        self._condition = condition
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

VARIABLE_TEMPLATE = re.compile('\\{(.+?)\\}')
def _evaluate_message(msg, args):
    '''
    >>> from decorated.base.dict import Dict
    >>> _evaluate_message('aaa', {})
    'aaa'
    >>> _evaluate_message('Id is {id}.', {'id':1})
    'Id is 1.'
    >>> _evaluate_message('Id is {user.id}.', {'user':Dict(id=1)})
    'Id is 1.'
    >>> _evaluate_message('Id is {user.id}.', {'user':Dict(id=1)})
    'Id is 1.'
    >>> _evaluate_message('Id is {!@#$%}.', {})
    'Id is {error:!@#$%}.'
    '''
    def _evaluate(matcher):
        expression = matcher.group(1)
        try:
            value = eval(expression, args) # pylint: disable=eval-used
            return str(value)
        except Exception:
            return '{error:%s}' % expression
    return VARIABLE_TEMPLATE.sub(_evaluate, msg)
    
LEVEL_MAPPING = {
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
MESSAGE_TEMPLATE = re.compile('\\[(\\w+)\\](.*)')
def _parse_expression(expression, default_level):
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
    match = MESSAGE_TEMPLATE.match(expression)
    if not match:
        return default_level, expression.strip()
    
    level, msg = match.groups()
    level = LEVEL_MAPPING.get(level.upper(), logging.WARN)
    msg = msg.strip()
    return level, msg
    
if __name__ == '__main__':
    doctest.testmod()
    