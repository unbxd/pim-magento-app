import os
from setuptools import setup, find_packages


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


VERSION = '0.1'

setup(
    name='app',
    version=VERSION,

    packages=find_packages(),

    url='https://github.com/unbxd/pas-template',

    author='Unbxd PIM',
    author_email='sivanv@unbxd.com',

    description='App Integration for Donde & Unbxd PIM App Platform',
    long_description=read('README.md'),
    license='MIT',

    keywords=['app', 'api', 'client'],
)