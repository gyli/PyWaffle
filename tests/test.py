#!/usr/bin/python
# -*-coding: utf-8 -*-

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle
import unittest


class TestWaffle(unittest.TestCase):
    def test_legend(self):
        fig = plt.figure(FigureClass=Waffle, rows=10, values=[10], labels=["cat1"])
        self.assertEqual(fig.gca().get_legend().texts[0]._text, 'cat1')


if __name__ == '__main__':
    unittest.main()
