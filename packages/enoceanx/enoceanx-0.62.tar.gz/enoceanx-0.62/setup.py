#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='enoceanx',
    version='0.62',
    description='EnOcean serial protocol implementation',
    author='Felix Beier',
    author_email='choleriker99@gmail.com',
    url='https://github.com/flexxor/enoceanx',
    packages=[
        'enoceanx',
        'enoceanx.protocol',
        'enoceanx.communicators',
    ],
    scripts=[
        'examples/enocean_example.py',
    ],
    package_data={
        '': ['EEP.xml']
    },
    install_requires=[
        'enum-compat>=0.0.2',
        'pyserial>=3.0',
        'beautifulsoup4>=4.3.2',
    ])
