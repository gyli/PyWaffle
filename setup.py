#!/usr/bin/python
# -*-coding: utf-8 -*-

from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open('README_pypi.rst') as f:
    long_description = f.read()

setup(
    name="pywaffle",
    description="PyWaffle is an open source, MIT-licensed Python package for plotting waffle charts.",
    keywords="matplotlib waffle chart pie plot data visualization",
    long_description=long_description,
    license='MIT',
    author="Guangyang Li",
    author_email="mail@guangyangli.com",
    url="https://github.com/gyli/PyWaffle",
    packages=['pywaffle'],
    install_requires=['matplotlib'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    package_data={
        'pywaffle': [
            'fontawesome/*',
        ]
    },
    include_package_data=True
)
