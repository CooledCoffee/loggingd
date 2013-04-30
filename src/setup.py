# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='loggingd',
    version='1.0.2',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
    description='Logging using decorators.',
    packages=['loggingd'],
    url='https://github.com/CooledCoffee/loggingd/',
    install_requires=[
        'decorated >= 1.0.0',
    ],
)
