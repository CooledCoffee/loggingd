# -*- coding: utf-8 -*-
from fixtures import TempDir
from logging import StreamHandler, FileHandler, Handler

from fixtures2 import TestCase

from loggingd import config

class TestHandler(Handler):
    pass

class CreateHandlerTest(TestCase):
    def test_stdout(self):
        config_ = {
            'type': 'stdout',
            'level': 'INFO',
            'format': '%(message)s',
        }
        handler = config._create_handler(config_)
        self.assertIsInstance(handler, StreamHandler)

    def test_stderr(self):
        config_ = {
            'type': 'stderr',
            'level': 'INFO',
            'format': '%(message)s',
        }
        handler = config._create_handler(config_)
        self.assertIsInstance(handler, StreamHandler)

    def test_file(self):
        # set up
        tempdir = self.useFixture(TempDir())

        # test
        config_ = {
            'type': 'file',
            'level': 'INFO',
            'format': '%(message)s',
            'path': tempdir.join('test.log'),
        }
        handler = config._create_handler(config_)
        self.assertIsInstance(handler, FileHandler)

    def test_customized(self):
        config_ = {
            'type': 'config_test.TestHandler',
            'level': 'INFO',
            'format': '%(message)s',
        }
        handler = config._create_handler(config_)
        self.assertIsInstance(handler, TestHandler)
