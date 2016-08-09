# -*- coding: utf-8 -*-
from fixtures import TempDir
from logging import StreamHandler, FileHandler, Handler

from fixtures2 import TestCase

from loggingd import util

class TestHandler(Handler):
    pass

class CreateHandlerTest(TestCase):
    def test_stdout(self):
        config = {
            'type': 'stdout',
            'level': 'INFO',
            'format': '%(message)s',
        }
        handler = util._create_handler(config)
        self.assertIsInstance(handler, StreamHandler)

    def test_stderr(self):
        config = {
            'type': 'stderr',
            'level': 'INFO',
            'format': '%(message)s',
        }
        handler = util._create_handler(config)
        self.assertIsInstance(handler, StreamHandler)

    def test_file(self):
        # set up
        tempdir = self.useFixture(TempDir())

        # test
        config = {
            'type': 'file',
            'level': 'INFO',
            'format': '%(message)s',
            'path': tempdir.join('test.log'),
        }
        handler = util._create_handler(config)
        self.assertIsInstance(handler, FileHandler)

    def test_customized(self):
        config = {
            'type': 'util_test.TestHandler',
            'level': 'INFO',
            'format': '%(message)s',
        }
        handler = util._create_handler(config)
        self.assertIsInstance(handler, TestHandler)
