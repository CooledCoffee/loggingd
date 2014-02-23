# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='loggingd',
    version='1.1.3',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Logging',
    ],
    description='Logging using decorators.',
    packages=['loggingd'],
    url='https://github.com/CooledCoffee/loggingd/',
    install_requires=[
        'decorated >= 1.2.1',
    ],
)
