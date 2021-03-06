# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

setup(
    name='loggingd',
    version='1.4.1',
    author='Mengchen LEE',
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
    description='Logging framework using decorators.',
    extras_require={
        'test': [
            'fixtures>=3.0.0',
            'fixtures2>=0.1.7',
        ],
    },
    install_requires=[
        'decorated>=1.6.2',
        'pyyaml>=3.11',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    url='https://github.com/cooledcoffee/loggingd'
)
