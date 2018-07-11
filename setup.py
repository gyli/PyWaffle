#!/usr/bin/python
# -*-coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README_pypi.rst') as f:
    long_description = f.read()

setup(
    name="pywaffle",
    version="0.0.9",
    description="A FigureClass of Matplotlib to make waffle chart.",
    keywords="matplotlib waffle chart pie plot data visualization",
    long_description=long_description,
    license='MIT',
    author="Guangyang Li",
    author_email="mail@guangyangli.com",
    url="https://github.com/ligyxy/PyWaffle",
    packages=['pywaffle', 'font'],
    install_requires=['matplotlib'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    package_data={'font': ['FontAwesome.otf']},
    include_package_data=True
)
