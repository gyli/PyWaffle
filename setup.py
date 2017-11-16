#!/usr/bin/python
# -*-coding: utf-8 -*-

from distutils.core import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.rst') as f:
    long_description = f.read()

setup(
    name="pywaffle",
    version="0.0.1",
    description="A FigureClass of Matplotlib to make waffle chart.",
    long_description=long_description,
    license='MIT',
    author="Guangyang Li",
    author_email="mail@guangyangli.com",
    url="https://www.guangayangli.com",
    packages=['pywaffle'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
