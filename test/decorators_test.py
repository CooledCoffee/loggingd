# -*- coding: utf-8 -*-
import logging

from decorated.base.dict import Dict
from fixtures2 import TestCase

import loggingd
from loggingd.decorators import Log, LogEnter, LogReturn, LogError, \
    LogAndIgnoreError


def foo(id, name='default name'):
    return id
        
class EvaluateExpressions(TestCase):
    def test_no_condition(self):
        decorated = Log('aaa')(foo)
        condition, msg = decorated._evaluate_expressions(None, None, 1, name='my name')
        self.assertTrue(condition)
        self.assertEquals('aaa', msg)
        
    def test_condition_true(self):
        decorated = Log('aaa', '1 == 1')(foo)
        condition, msg = decorated._evaluate_expressions(None, None, 1, name='my name')
        self.assertTrue(condition)
        self.assertEquals('aaa', msg)
        
    def test_condition_false(self):
        decorated = Log('aaa', '1 == 2')(foo)
        condition, msg = decorated._evaluate_expressions(None, None, 1, name='my name')
        self.assertFalse(condition)
        self.assertIsNone(msg)
        
    def test_extra_kw_in_condition(self):
        decorated = Log('aaa', 'ret')(foo)
        condition, _ = decorated._evaluate_expressions([1], {'name': 'my name'}, {'ret': True})
        self.assertTrue(condition)
        
    def test_extra_kw_in_msg(self):
        decorated = Log('aaa {ret} bbb')(foo)
        _, msg = decorated._evaluate_expressions('111', None, 1, name='my name')
        self.assertEquals('aaa 111 bbb', msg)
        
    def test_bad_condition(self):
        decorated = Log('aaa', '!@#$%')(foo)
        condition, msg = decorated._evaluate_expressions(None, None, 1, name='my name')
        self.assertTrue(condition)
        self.assertEquals('Invalid condition: !@#$%.', msg)
        
    def test_bad_msg(self):
        decorated = Log('aaa {bbb} ccc')(foo)
        condition, msg = decorated._evaluate_expressions(None, None, 1, name='my name')
        self.assertTrue(condition)
        self.assertEquals('aaa {error:bbb} ccc', msg)
        
class BaseLoggerTest(TestCase):
    def setUp(self):
        super(BaseLoggerTest, self).setUp()
        loggingd.init()
        self._old_get_logger = logging.getLogger
        self.logs = logs = []
        class _Logger(object):
            def log(self, level, msg, exc_info=None):
                logs.append(Dict(level=level, msg=msg, exc_info=exc_info))
        def _get_logger(name):
            return _Logger()
        logging.getLogger = _get_logger
        
    def tearDown(self):
        logging.getLogger = self._old_get_logger
        super(BaseLoggerTest, self).tearDown()
        
class LogTest(BaseLoggerTest):
    def test_simple(self):
        # test
        decorated = Log('{id}')(foo)
        decorated._log(None, None, 1)
            
        # verify
        self.assertEquals(1, len(self.logs))
        self.assertEquals(logging.INFO, self.logs[0].level)
        self.assertEquals('1', self.logs[0].msg)
        self.assertIsNone(self.logs[0].exc_info)
             
    def test_exc_info(self):
        decorated = Log('{id}', exc_info=True)(foo)
        try:
            raise Exception()
        except:
            decorated._log(None, None, 1)
                
        # verify
        self.assertEquals(1, len(self.logs))
        self.assertEquals(logging.INFO, self.logs[0].level)
        self.assertEquals('1', self.logs[0].msg)
        self.assertTrue(self.logs[0].exc_info)
         
class LogEnterTest(BaseLoggerTest):
    def test_simple(self):
        # test
        @LogEnter('aaa')
        def _foo():
            return 1
        ret = _foo()
        
        # verify
        self.assertEquals(1, ret)
        self.assertEquals(1, len(self.logs))
        self.assertEquals(logging.INFO, self.logs[0].level)
        self.assertEquals('aaa', self.logs[0].msg)
         
    def test_multi(self):
        @LogEnter('aaa')
        @LogEnter('bbb')
        def _foo():
            pass
        _foo()
            
        # verify
        self.assertEquals(2, len(self.logs))
        self.assertEquals(logging.INFO, self.logs[0].level)
        self.assertEquals('aaa', self.logs[0].msg)
        self.assertEquals(logging.INFO, self.logs[1].level)
        self.assertEquals('bbb', self.logs[1].msg)
             
    def test_conditional(self):
        # test
        @LogEnter('aaa', 'id==111')
        @LogEnter('bbb', 'id==222')
        def _foo(id):
            pass
        _foo(222)
        
        # verify
        self.assertEquals(1, len(self.logs))
        self.assertEquals(logging.INFO, self.logs[0].level)
        self.assertEquals('bbb', self.logs[0].msg)

class LogReturnTest(BaseLoggerTest):
    def test_success(self):
        # test
        @LogReturn('Id is {id}, return is {ret}.')
        def _foo(id):
            return 1
        _foo(111)
        
        # verify
        self.assertEquals(1, len(self.logs))
        self.assertEquals(logging.INFO, self.logs[0].level)
        self.assertEquals('Id is 111, return is 1.', self.logs[0].msg)
             
    def test_error(self):
        # test
        @LogReturn('aaa')
        def _foo(id):
            raise Exception()
        with self.assertRaises(Exception):
            _foo(111)
            
        # verify
        self.assertEquals(0, len(self.logs))
             
class LogErrorTest(BaseLoggerTest):
    def test_success(self):
        # test
        @LogError('aaa')
        def _foo(id):
            return 1
        _foo(111)
        
        # verify
        self.assertEquals(0, len(self.logs))
             
    def test_error(self):
        # test
        @LogError('Id is {id}, error is {e}.', exc_info=True)
        def _foo(id):
            raise Exception('aaa')
        with self.assertRaises(Exception):
            _foo(111)

        # verify
        self.assertEquals(1, len(self.logs))
        self.assertEquals(logging.WARN, self.logs[0].level)
        self.assertEquals('Id is 111, error is aaa.', self.logs[0].msg)
        
class LogAndIgnoreErrorTest(BaseLoggerTest):
    def test_success(self):
        # test
        @LogAndIgnoreError('aaa')
        def _foo(id):
            return 1
        result = _foo(111)
        
        # verify
        self.assertEqual(1, result)
        self.assertEquals(0, len(self.logs))
        
    def test_error(self):
        # test
        @LogAndIgnoreError('Id is {id}, error is {e}.', exc_info=True)
        def _foo(id):
            raise Exception('aaa')
        result = _foo(111)

        # verify
        self.assertIsNone(result)
        self.assertEquals(1, len(self.logs))
        self.assertEquals(logging.WARN, self.logs[0].level)
        self.assertEquals('Id is 111, error is aaa.', self.logs[0].msg)

    def test_errors(self):
        # test
        @LogAndIgnoreError('aaa', error_classes=(ArithmeticError,))
        def _foo(id):
            raise TypeError()

        with self.assertRaises(TypeError):
            result = _foo(111)
