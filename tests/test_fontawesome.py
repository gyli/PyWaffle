#!/usr/bin/python
# -*-coding: utf-8 -*-

import unittest

from pywaffle.fontawesome_handler import FA_STYLES, font_file_finder


class TestFontFileFinder(unittest.TestCase):
    def test_font_file_finder(self):
        font_file_mapping = font_file_finder()

        self.assertTrue(font_file_mapping["brands"].name.endswith("Brands-Regular-400.otf"))

        # Compare path segments rather than a substring, so the assertion holds on Windows too
        parts = font_file_mapping["brands"].resolve().parts
        self.assertEqual(parts[-5:-1], ("fontawesomefree", "static", "fontawesomefree", "otfs"))
        self.assertTrue(parts[-1].endswith(".otf"))

    def test_every_style_resolves_to_an_existing_file(self):
        font_file_mapping = font_file_finder()
        self.assertEqual(set(font_file_mapping), set(FA_STYLES))
        for style, path in font_file_mapping.items():
            with self.subTest(style=style):
                self.assertTrue(path.is_file(), f"{style} font file is missing: {path}")


if __name__ == "__main__":
    unittest.main()
