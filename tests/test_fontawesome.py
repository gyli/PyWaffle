#!/usr/bin/python
# -*-coding: utf-8 -*-

import unittest

from pywaffle.fontawesome_handler import font_file_finder


class TestUtilities(unittest.TestCase):
    def test_font_file_finder(self):
        font_file_mapping = font_file_finder()
        self.assertEqual(
            font_file_mapping["brands"].name.endswith("Brands-Regular-400.otf"), True
        )
        self.assertIn(
            "/fontawesomefree/static/fontawesomefree/otfs/",
            str(font_file_mapping["brands"].resolve()),
        )


if __name__ == "__main__":
    unittest.main()
