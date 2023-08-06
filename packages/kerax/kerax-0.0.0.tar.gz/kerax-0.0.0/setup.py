#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='kerax',
    version='0.0.0',
    description='kerax',
    long_description='kerax',
    license='Apache License 2.0',
    url='https://github.com/bojone/kerax',
    author='bojone',
    author_email='bojone@spaces.ac.cn',
    install_requires=['jax'],
    packages=find_packages()
)
