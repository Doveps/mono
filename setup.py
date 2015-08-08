from setuptools import setup, find_packages

setup(
    name='bassist',
    version='0.0.1dev',
    packages=find_packages(),
    scripts=['bin/create_automation', 'bin/create_flavor'],
    long_description=open('README.md').read(),
)

