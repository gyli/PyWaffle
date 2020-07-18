#!/usr/bin/python
# -*-coding: utf-8 -*-

import os
import unittest

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle


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

    def test_block_arranger(self):
        self.assertEqual(
            list(Waffle.block_arranger(rows=2, columns=3, row_order=1, column_order=1, is_vertical=False)),
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
        )
        self.assertEqual(
            list(Waffle.block_arranger(rows=2, columns=3, row_order=-1, column_order=1, is_vertical=True)),
            [(0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0)],
        )
        self.assertEqual(
            list(Waffle.block_arranger(rows=0, columns=0, row_order=1, column_order=1, is_vertical=True)), []
        )

    def test_legend(self):
        fig = plt.figure(FigureClass=Waffle, rows=10, values=[10], labels=["cat1"])
        self.assertEqual(fig.gca().get_legend().texts[0]._text, "cat1")

    def test_plot(self):
        test_plots_folder = "test_plots/"

        # Most of parameters
        data = {"Democratic": 48, "Republican": 46, "Libertarian": 3}
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=data,
            colors=("#983D3D", "#232066", "#DCB732"),
            title={"label": "Vote Percentage in 2016 US Presidential Election", "loc": "left"},
            labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
            legend={"loc": "lower left", "bbox_to_anchor": (0, -0.4), "ncol": len(data), "framealpha": 0},
            starting_location="NW",
        )
        fig.savefig(test_plots_folder + "title_and_legend.png", bbox_inches="tight", facecolor="#EEEEEE")

        # Test positions
        fig = plt.figure(
            FigureClass=Waffle,
            plots={
                "311": {"values": [10, 10, 10],},
                312: {"values": [10, 10, 10],},
                (3, 1, 3): {"values": [10, 10, 10],},
            },
            rows=5,
        )
        fig.savefig(test_plots_folder + "subplot_types.png", bbox_inches="tight")

        self.assertTrue(os.path.exists(test_plots_folder + "subplot_types.png"))


if __name__ == "__main__":
    unittest.main()
