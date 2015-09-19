import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-expiring-tokens',
    version='0.1.2',
    description='Add an API to your Django app using token-based authentication. Tokens expire on subsequent logins.',
    long_description=read('README.md'),
    author='Stephen Hebson',
    author_email='stephen.hebson@gmail.com',
    url='https://github.com/shebson/django-expiring-tokens',
    packages=['tokenapi'],
    license='Apache License, Version 2.0',
)
