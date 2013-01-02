#!/usr/bin/env python
import os

__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup

setup(
    name='yapa',
    version=__version__,
    description='Yet Another Python Apriori Algorithm',
    #long_description=long_description,
    url='http://github.com/ncloudioj/apriori',
    author='Nan Jiang',
    author_email='njiang028@gmail.com',
    maintainer='Nan Jiang',
    maintainer_email='njiang028@gmail.com',
    keywords=['Apriori', 'Association Rule'],
    packages=['yapa'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ]
)
