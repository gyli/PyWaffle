#!/usr/bin/python
# -*-coding: utf-8 -*-

from pathlib import Path

from setuptools import setup
from setuptools.command.install import install

from scripts import fontawesome_mapping_generator


class InstallCommand(install):
    # Generate Font Awesome mapping file after install, so it can fit multiple versions
    def run(self):
        install.run(self)
        fontawesome_mapping_generator.main()


with open(Path(__file__).parent.absolute() / "README_pypi.rst") as f:
    long_description = f.read()

setup(
    name="pywaffle",
    description="PyWaffle is an open source, MIT-licensed Python package for plotting waffle charts.",
    keywords="matplotlib waffle chart pie plot data visualization",
    long_description=long_description,
    license="MIT",
    author="Guangyang Li",
    author_email="mail@guangyangli.com",
    url="https://github.com/gyli/PyWaffle",
    packages=["pywaffle"],
    install_requires=["fontawesomefree", "matplotlib"],
    cmdclass={"install": InstallCommand},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Console',
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
