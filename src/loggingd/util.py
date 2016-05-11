# -*- coding: utf-8 -*-
import doctest
import importlib

_MODULE_BLACKLIST = set()
_PATH_BLACKLIST = set()

def disable_module_log(module_name):
    global _MODULE_BLACKLIST, _PATH_BLACKLIST
    _MODULE_BLACKLIST.add(module_name)
    _PATH_BLACKLIST = {importlib.import_module(mod).__file__ for mod in _MODULE_BLACKLIST}
    
if __name__ == '__main__':
    doctest.testmod()
    