# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from setuptools import setup, find_packages

setup(
    name='bassist',
    version='0.0.1dev',
    packages=find_packages(),
    scripts=['bin/create_automation'],
    long_description=open('README.md').read(),
)

