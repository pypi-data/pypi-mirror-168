#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages

setup(
    name='bioflowgraph',
    version='0.0.1',
    author='barwe',
    author_email='barwechin@163.com',
    url='',
    description='',
    # packages=find_packages(exclude=['test', 'tmp', 'test.py']),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'exuse==0.1.3',
        'graphviz==0.20.1',
        'psutil==5.9.2',
        'toml==0.10.2',
        'typing_extensions==4.3.0'
    ],
)
