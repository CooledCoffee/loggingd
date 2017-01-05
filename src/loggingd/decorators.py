# -*- coding: UTF-8 -*-
from decorated import WrapperFunction
import doctest
import logging
import re

class Log(WrapperFunction):
    default_level = logging.INFO
    
    def _evaluate_expressions(self, ret, e, *args, **kw):
        d = self._resolve_args(*args, **kw)
        d['ret'] = ret
        d['e'] = e
        try:
            condition = eval(self._condition, d)
        except Exception:
            return True, 'Invalid condition: %s.' % self._condition
        if condition:
            return True, _evaluate_message(self._msg, d)
        else:
            return False, None
    
    def _init(self, expression, condition='True', **kw):
        super(Log, self)._init()
        self._level, self._msg = _parse_expression(expression, self.default_level)
        self._condition = condition
        self._extra_kw = kw
            
    def _log(self, ret, e, *args, **kw):
        condition, msg = self._evaluate_expressions(ret, e, *args, **kw)
        if condition:
            logger = logging.getLogger(self.__module__)
            logger.log(self._level, msg, exc_info=self._extra_kw.get('exc_info'))
                
class LogEnter(Log):
    def _before(self, *args, **kw):
        self._log(None, None, *args, **kw)
    
class LogReturn(Log):
    def _after(self, ret, *args, **kw):
        self._log(ret, None, *args, **kw)
    
class LogError(Log):
    default_level = logging.WARN
    
    def _error(self, error, *args, **kw):
        self._log(None, error, *args, **kw)
    
class LogAndIgnoreError(LogError):
    def _init(self, *args, **kw):
        if 'error_classes' in kw:
            self._error_classes = kw.pop('error_classes')
        else:
            self._error_classes = Exception
        super(LogAndIgnoreError, self)._init(*args, **kw)

    def _call(self, *args, **kw):
        try:
            return super(LogAndIgnoreError, self)._call(*args, **kw)
        except Exception as e:
            if not isinstance(e, self._error_classes):
                raise

VARIABLE_TEMPLATE = re.compile('\\{(.+?)\\}')
def _evaluate_message(msg, d):
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
            value = eval(expression, d)
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
    