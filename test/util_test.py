# -*- coding: utf-8 -*-
from decorated import function
from loggingd import util
from loggingd.util import Dict
from unittest.case import TestCase
import importlib
import loggingd
import os

class ModifyFrameTest(TestCase):
    def setUp(self):
        super(ModifyFrameTest, self).setUp()
        loggingd.init()
        
    def test_black_frames_on_top(self):
        # set up
        black_path = os.path.abspath(function.__file__).rstrip('c')
        frame4 = Dict(tb_frame=Dict(f_code=Dict(co_filename='logic module path')),
                tb_lasti=111,
                tb_lineno=111,
                tb_next=None)
        frame3 = Dict(tb_frame=Dict(f_code=Dict(co_filename='logic module path')),
                tb_lasti=222,
                tb_lineno=222,
                tb_next=frame4)
        frame2 = Dict(tb_frame=Dict(f_code=Dict(co_filename=black_path)),
                tb_lasti=333,
                tb_lineno=333,
                tb_next=frame3)
        frame1 = Dict(tb_frame=Dict(f_code=Dict(co_filename=black_path)),
                tb_lasti=444,
                tb_lineno=444,
                tb_next=frame2)
        
        # test
        frame = util._modify_frame(frame1)
        self.assertEquals('logic module path', frame.tb_frame.f_code.co_filename)
        self.assertEquals('logic module path', frame.tb_next.tb_frame.f_code.co_filename)
        self.assertIsNone(frame.tb_next.tb_next)
        
    def test_black_frames_on_bottom(self):
        # set up
        black_path = os.path.abspath(function.__file__).rstrip('c')
        frame4 = Dict(tb_frame=Dict(f_code=Dict(co_filename=black_path)),
                tb_lasti=111,
                tb_lineno=111,
                tb_next=None)
        frame3 = Dict(tb_frame=Dict(f_code=Dict(co_filename=black_path)),
                tb_lasti=222,
                tb_lineno=222,
                tb_next=frame4)
        frame2 = Dict(tb_frame=Dict(f_code=Dict(co_filename='logic module path')),
                tb_lasti=333,
                tb_lineno=333,
                tb_next=frame3)
        frame1 = Dict(tb_frame=Dict(f_code=Dict(co_filename='logic module path')),
                tb_lasti=444,
                tb_lineno=444,
                tb_next=frame2)
         
        # test
        frame = util._modify_frame(frame1)
        self.assertEquals('logic module path', frame.tb_frame.f_code.co_filename)
        self.assertEquals('logic module path', frame.tb_next.tb_frame.f_code.co_filename)
        self.assertIsNone(frame.tb_next.tb_next)
        
    def test_black_frames_in_middle(self):
        # set up
        black_path = os.path.abspath(function.__file__).rstrip('c')
        frame4 = Dict(tb_frame=Dict(f_code=Dict(co_filename='logic module path')),
                tb_lasti=111,
                tb_lineno=111,
                tb_next=None)
        frame3 = Dict(tb_frame=Dict(f_code=Dict(co_filename=black_path)),
                tb_lasti=222,
                tb_lineno=222,
                tb_next=frame4)
        frame2 = Dict(tb_frame=Dict(f_code=Dict(co_filename=black_path)),
                tb_lasti=333,
                tb_lineno=333,
                tb_next=frame3)
        frame1 = Dict(tb_frame=Dict(f_code=Dict(co_filename='logic module path')),
                tb_lasti=444,
                tb_lineno=444,
                tb_next=frame2)
         
        # test
        frame = util._modify_frame(frame1)
        self.assertEquals('logic module path', frame.tb_frame.f_code.co_filename)
        self.assertEquals('logic module path', frame.tb_next.tb_frame.f_code.co_filename)
        self.assertIsNone(frame.tb_next.tb_next)
        