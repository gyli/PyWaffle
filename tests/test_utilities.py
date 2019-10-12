#!/usr/bin/python
# -*-coding: utf-8 -*-

from pywaffle.waffle import array_resize, division
import unittest


class TestUtilities(unittest.TestCase):
    def test_array_resize(self):
        self.assertEqual(array_resize(array=[1, 2, 3, 4, 5], length=2), [1, 2])
        self.assertEqual(array_resize(array=[1, 2, 3, 4, 5], length=2, array_len=5), [1, 2])
        self.assertEqual(array_resize(array=[1, 2], length=5, array_len=2), [1, 2, 1, 2, 1])

    def test_utilities(self):
        self.assertEqual(division(x=2, y=3, method="float"), 2 / 3)
        self.assertIsInstance(division(x=2, y=3, method="float"), float)

        self.assertEqual(division(x=2, y=3, method="nearest"), 1)
        self.assertIsInstance(division(x=2, y=3, method="nearest"), int)

        self.assertEqual(division(x=2, y=3, method="ceil"), 1)
        self.assertIsInstance(division(x=2, y=3, method="ceil"), int)

        self.assertEqual(division(x=2, y=3, method="floor"), 0)
        self.assertIsInstance(division(x=2, y=3, method="floor"), int)
