# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from setuptools import setup, find_packages

setup(
    name='savant',
    version='0.0.1dev',
    packages=find_packages(),
    scripts=['bin/set_savant_password'],
    long_description=open('README.md').read(),
)
