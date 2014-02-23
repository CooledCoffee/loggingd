# -*- coding: utf-8 -*-
from decorated.base.dict import Dict
from logging import Logger
import doctest
import importlib
import sys

_MODULE_BLACKLIST = set()
_PATH_BLACKLIST = set()

def disable_module_log(module_name):
    global _MODULE_BLACKLIST, _PATH_BLACKLIST
    _MODULE_BLACKLIST.add(module_name)
    _PATH_BLACKLIST = {importlib.import_module(mod).__file__ for mod in _MODULE_BLACKLIST}
    
def patch_logging():
    old_log = Logger._log
    def _log(self, level, msg, args, exc_info=None, extra=None):
        if exc_info:
            exc_info = _get_exc_info()
        old_log(self, level, msg, args, exc_info, extra)
    Logger._log = _log
    
def _get_exc_info():
    exc_info = sys.exc_info()
    traceback = exc_info[2]
    if traceback:
        traceback = _modify_frame(traceback)
        return (exc_info[0], exc_info[1], traceback)
    else:
        # no error thus exc_info is (None, None, None)
        return exc_info
        
def _modify_frame(frame):
    if frame is None:
        return frame
    frame = _tag_frame(frame)
    frame.tb_next = _modify_frame(frame.tb_next)
    return frame if not frame.black else frame.tb_next

def _tag_frame(frame):
    # tag frame as black or white
    black = frame.tb_frame.f_code.co_filename in _PATH_BLACKLIST
    return Dict(tb_frame=frame.tb_frame,
                tb_lasti=frame.tb_lasti,
                tb_lineno=frame.tb_lineno,
                tb_next=frame.tb_next,
                black=black)
    
if __name__ == '__main__':
    doctest.testmod()
    