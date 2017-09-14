# -*- coding: utf-8 -*-
import importlib
import logging
import sys
from logging import FileHandler, Formatter, StreamHandler

import yaml

DEFAULT_FORMAT = '[%(asctime)s] [%(levelname)s] [%(process)d:%(threadName)s] ' \
                 '[%(name)s:%(funcName)s:%(lineno)d]\n%(message)s'

def add_console_handler(level, fmt=DEFAULT_FORMAT):
    handler = StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(Formatter(fmt))
    logging.getLogger().addHandler(handler)

def add_file_handler(level, path, fmt=DEFAULT_FORMAT):
    logger = logging.getLogger()
    handler = FileHandler(path)
    handler.setLevel(level)
    handler.setFormatter(Formatter(fmt))
    logger.addHandler(handler)

def init(level=logging.INFO):
    logging.getLogger().setLevel(level)

def yaml_config(config):
    config = yaml.load(config)
    init(config['level'])
    for handler in config['handlers']:
        handler = _create_handler(handler)
        logging.getLogger().addHandler(handler)

def _create_handler(config):
    type_ = config.pop('type')
    level = config.pop('level', 'INFO')
    try:
        level = getattr(logging, level)
    except AttributeError:
        raise Exception('Level "%s" is undefined.' % level)
    fmt = config.pop('format', DEFAULT_FORMAT)
    if type_ == 'stdout':
        handler = StreamHandler(stream=sys.stdout)
    elif type_ == 'stderr':
        handler = StreamHandler(stream=sys.stderr)
    elif type_ == 'file':
        handler = FileHandler(config['path'])
    else:
        cls = _obj_from_path(type_)
        handler = cls(**config)
    handler.setLevel(level)
    handler.setFormatter(Formatter(fmt))
    return handler

def _obj_from_path(path):
    '''
    >>> obj = _obj_from_path('loggingd.config._obj_from_path')
    >>> obj.__name__
    '_obj_from_path'
    '''
    mod, attr = path.rsplit('.', 1)
    mod = importlib.import_module(mod)
    return getattr(mod, attr)
