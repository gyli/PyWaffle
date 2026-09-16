#!/usr/bin/python
# -*-coding: utf-8 -*-

from ._version import __version__
from .functional import waffle
from .waffle import Waffle

__all__ = ["Waffle", "waffle", "__version__"]
