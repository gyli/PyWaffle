#!/usr/bin/python
# -*-coding: utf-8 -*-

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle
import unittest


class TestWaffle(unittest.TestCase):
    def test_parameters(self):
        values = [10, 20]
        fig = plt.figure(
            FigureClass=Waffle, rows=10, values=values, icons="star", icon_style="solid", labels=["cat1", "cat2"]
        )
        self.assertEqual(fig._pa["values"], values)
        self.assertEqual(fig._pa["rows"], 10)
        self.assertEqual(fig._pa["icons"], ["\uf005", "\uf005"])  # star => \uf005
        self.assertEqual(fig._pa["icon_style"], ["solid", "solid"])

        # Default values
        self.assertEqual(fig._pa["interval_ratio_x"], 0.2)
        self.assertEqual(fig._pa["interval_ratio_y"], 0.2)
        self.assertEqual(fig._pa["block_aspect_ratio"], 1)
        self.assertEqual(fig._pa["plot_anchor"], "W")
        self.assertEqual(fig._pa["starting_location"], "SW")
        self.assertEqual(fig._pa["rounding_rule"], "nearest")

        self.assertEqual(fig.values_len, len(values))
        self.assertEqual(fig.value_sum, 30)

    def test_legend(self):
        fig = plt.figure(FigureClass=Waffle, rows=10, values=[10], labels=["cat1"])
        self.assertEqual(fig.gca().get_legend().texts[0]._text, "cat1")


if __name__ == "__main__":
    unittest.main()
