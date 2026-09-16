#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Font Awesome is an optional dependency, so the package has to behave without it."""

import builtins
import importlib.util
import sys
import unittest
from unittest import mock

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pywaffle.fontawesome_handler import MISSING_FONT_AWESOME
from pywaffle.waffle import Waffle


def without_fontawesome():
    """Make importing fontawesomefree fail, as it would for someone who did not install the extra.

    The real import is cached in sys.modules and the resolved fonts are cached by lru_cache, so
    both have to be cleared for the absence to be visible.
    """
    real_import = builtins.__import__

    def refuse(name, *args, **kwargs):
        if name == "fontawesomefree":
            raise ImportError("No module named 'fontawesomefree'")
        return real_import(name, *args, **kwargs)

    return mock.patch.object(builtins, "__import__", refuse)


class TestWithoutFontAwesome(unittest.TestCase):
    """What a user who ran plain `pip install pywaffle` sees."""

    def setUp(self):
        from pywaffle import fontawesome_handler

        self.handler = fontawesome_handler
        # Clear anything a previous test resolved, and restore it afterwards
        self.cached = {k: fontawesome_handler.__dict__.pop(k, None) for k in fontawesome_handler._LAZY}
        fontawesome_handler.font_file_finder.cache_clear()
        fontawesome_handler.icon_mapping_builder.cache_clear()
        self.saved_module = sys.modules.pop("fontawesomefree", None)

    def tearDown(self):
        for name, value in self.cached.items():
            if value is not None:
                self.handler.__dict__[name] = value
        if self.saved_module is not None:
            sys.modules["fontawesomefree"] = self.saved_module
        plt.close("all")

    def test_rectangle_charts_still_work(self):
        """The common case does not involve icons and must not require the font package."""
        with without_fontawesome():
            fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20])
        self.assertEqual(len(fig.axes[0].patches), 30)

    def test_characters_still_work(self):
        """Characters use the system font, not Font Awesome."""
        with without_fontawesome():
            fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], characters="*")
        self.assertEqual(len(fig.axes[0].texts), 30)

    def test_icons_raise_importerror_with_instructions(self):
        """A bare ModuleNotFoundError tells the user nothing about what to install."""
        with without_fontawesome():
            with self.assertRaises(ImportError) as caught:
                plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], icons="star")
        message = str(caught.exception)
        self.assertIn("pywaffle[icons]", message)
        self.assertIn("fontawesomefree", message)

    def test_the_message_is_the_shared_one(self):
        """One message, so the install instructions cannot drift between call sites."""
        with without_fontawesome():
            with self.assertRaises(ImportError) as caught:
                plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], icons="star")
        self.assertEqual(str(caught.exception), MISSING_FONT_AWESOME)

    def test_the_handler_module_still_imports(self):
        """_parameter_validation imports it just to read FA_STYLES, before any font is needed."""
        with without_fontawesome():
            from pywaffle.fontawesome_handler import FA_STYLES

            self.assertEqual(set(FA_STYLES), {"brands", "solid", "regular"})


HAS_FONT_AWESOME = importlib.util.find_spec("fontawesomefree") is not None


@unittest.skipIf(not HAS_FONT_AWESOME, "the icons extra is not installed")
class TestWithFontAwesome(unittest.TestCase):
    """With the extra installed, nothing about icons changes."""

    @staticmethod
    def tearDown():
        """Close the figures each test leaves behind."""
        plt.close("all")

    def test_icons_draw(self):
        """The whole point of the extra."""
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], icons="star")
        self.assertEqual(len(fig.axes[0].texts), 30)

    def test_lazy_attributes_resolve(self):
        """The module attributes are resolved on first access rather than at import."""
        from pywaffle import fontawesome_handler

        self.assertGreater(len(fontawesome_handler.icons["solid"]), 1000)
        self.assertEqual(set(fontawesome_handler.fontawesome_files), {"brands", "solid", "regular"})
        self.assertTrue(fontawesome_handler.legend_handler_style_mapping)

    def test_unknown_attribute_still_raises_attributeerror(self):
        """The lazy hook must not swallow genuine typos."""
        from pywaffle import fontawesome_handler

        with self.assertRaises(AttributeError):
            fontawesome_handler.no_such_attribute


if __name__ == "__main__":
    unittest.main()
