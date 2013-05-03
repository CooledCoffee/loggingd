# -*- coding: UTF-8 -*-
from decorated import Function
import doctest
import logging
import re

class LogDecorator(Function):
    default_level = logging.INFO
    
    def __init__(self, expression, condition='True', **kw):
        super(LogDecorator, self).__init__()
        self._level, self._msg = _parse_expression(expression, self.default_level)
        self._condition = condition
        self._extra_kw = kw
            
    def _evaluate_expressions(self, ret, e, *args, **kw):
        d = self._resolve_args(*args, **kw)
        d['ret'] = ret
        d['e'] = e
        try:
            condition = eval(self._condition, d)
        except:
            return True, 'Invalid condition: %s.' % self._condition
        if condition:
            return True, _evaluate_message(self._msg, d)
        else:
            return False, None
    
    def _log(self, ret, e, *args, **kw):
        condition, msg = self._evaluate_expressions(ret, e, *args, **kw)
        if condition:
            logger = logging.getLogger(self.__module__)
            logger.log(self._level, msg, exc_info=self._extra_kw.get('exc_info'))
                
class log_enter(LogDecorator):
    def _call(self, *args, **kw):
        self._log(None, None, *args, **kw)
        return super(log_enter, self)._call(*args, **kw)
    
class log_exit(LogDecorator):
    log_on_return = True
    log_on_error = True
    
    def _call(self, *args, **kw):
        try:
            ret = super(log_exit, self)._call(*args, **kw)
            if self.log_on_return:
                self._log(ret, None, *args, **kw)
            return ret
        except Exception as e:
            if self.log_on_error:
                self._log(None, e, *args, **kw)
            raise
    
class log_return(log_exit):
    log_on_error = False
    
class log_error(log_exit):
    log_on_return = False
    default_level = logging.WARN

VARIABLE_TEMPLATE = re.compile('\\{(.+?)\\}')
def _evaluate_message(msg, d):
    '''
    >>> from loggingd.util import Dict
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
        except:
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
    