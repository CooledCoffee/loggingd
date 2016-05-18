# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

setup(
    name='loggingd',
    version='1.2.4',
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
    description='Logging framework using decorators.',
    install_requires=[
        'decorated>=1.6.2',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    url='https://package-insights.appspot.com/packages/loggingd'
)
