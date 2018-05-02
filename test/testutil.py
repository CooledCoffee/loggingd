# -*- coding: utf-8 -*-
from decorated.base.function import Function
from decorated.testing import DecoratedFixture
from fixtures2 import TestCase


class LoggingdTest(TestCase):
    # noinspection PyAttributeOutsideInit
    def setUp(self):
        super(LoggingdTest, self).setUp()
        self.decorated = DecoratedFixture()
        self.decorated.enable(Function)
