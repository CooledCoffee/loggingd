# -*- coding: UTF-8 -*-
from decorated import Function
from logging import DEBUG, INFO, WARN, ERROR, CRITICAL
import doctest
import logging
import re

class LogDecorator(Function):
    DEFAULT_LEVEL = INFO
    LEVEL_MAPPING = {
            'DEBUG' : DEBUG,
            'INFO' : INFO,
            'WARN' : WARN,
            'ERROR' : ERROR,
            'CRITICAL' : CRITICAL,
            'D' : DEBUG,
            'I' : INFO,
            'W' : WARN,
            'E' : ERROR,
            'C' : CRITICAL,
    }
    
    def __init__(self, expression, condition='True', **kw):
        super(LogDecorator, self).__init__()
        self._level, self._msg = self._parse_expression(expression)
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
            return True, self._evaluate_message(d)
        else:
            return False, None
    
    def _evaluate_message(self, variables):
        '''
        >>> from loggingd.util import Dict
        >>> LogDecorator('aaa')._evaluate_message({})
        'aaa'
        >>> LogDecorator('Id is {id}.')._evaluate_message({'id':1})
        'Id is 1.'
        >>> LogDecorator('Id is {user.id}.')._evaluate_message({'user':Dict(id=1)})
        'Id is 1.'
        >>> LogDecorator('Id is {user.id}.')._evaluate_message({'user':Dict(id=1)})
        'Id is 1.'
        >>> LogDecorator('Id is {!@#$%}.')._evaluate_message({})
        'Id is {error:!@#$%}.'
        '''
        def _evaluate(matcher):
            expression = matcher.group(1)
            try:
                value = eval(expression, variables)
                return str(value)
            except:
                return '{error:%s}' % expression
        return re.sub('\\{(.+?)\\}', _evaluate, self._msg)
                
    def _log(self, ret, e, *args, **kw):
        condition, msg = self._evaluate_expressions(ret, e, *args, **kw)
        if condition:
            logger = logging.getLogger(self.__module__)
            logger.log(self._level, msg, exc_info=self._extra_kw.get('exc_info'))
                
    def _parse_expression(self, expression):
        match = re.match('\\[(\\w+)\\](.*)', expression)
        if not match:
            return self.DEFAULT_LEVEL, expression.strip()
        level, msg = match.groups()
        level = LogDecorator.LEVEL_MAPPING.get(level.upper(), WARN)
        msg = msg.strip()
        return level, msg
        
class log_enter(LogDecorator):
    def _call(self, *args, **kw):
        self._log(None, None, *args, **kw)
        return super(log_enter, self)._call(*args, **kw)
    
class log_exit(LogDecorator):
    LOG_ON_RETURN = True
    LOG_ON_ERROR = True
    
    def _call(self, *args, **kw):
        try:
            ret = super(log_exit, self)._call(*args, **kw)
            if self.LOG_ON_RETURN:
                self._log(ret, None, *args, **kw)
            return ret
        except Exception as e:
            if self.LOG_ON_ERROR:
                self._log(None, e, *args, **kw)
            raise
    
class log_return(log_exit):
    LOG_ON_RETURN = True
    LOG_ON_ERROR = False
    
class log_error(log_exit):
    LOG_ON_RETURN = False
    LOG_ON_ERROR = True
    DEFAULT_LEVEL = WARN

if __name__ == '__main__':
    doctest.testmod()
    