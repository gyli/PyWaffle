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
        self.assertEqual(fig.plot_args[0]["values"], values)
        self.assertEqual(fig.plot_args[0]["rows"], 10)
        self.assertEqual(fig.plot_args[0]["icons"], ["\uf005", "\uf005"])  # star => \uf005
        self.assertEqual(fig.plot_args[0]["icon_style"], ["solid", "solid"])

        # Default values
        self.assertEqual(fig.plot_args[0]["interval_ratio_x"], 0.2)
        self.assertEqual(fig.plot_args[0]["interval_ratio_y"], 0.2)
        self.assertEqual(fig.plot_args[0]["block_aspect_ratio"], 1)
        self.assertEqual(fig.plot_args[0]["plot_anchor"], "W")
        self.assertEqual(fig.plot_args[0]["starting_location"], "SW")
        self.assertEqual(fig.plot_args[0]["rounding_rule"], "nearest")

        self.assertEqual(fig.values_len, len(values))

        # subplot parameter overwriting
        fig = plt.figure(
            FigureClass=Waffle,
            rows=10,
            values=values,
            labels=["cat1", "cat2"],
            plots={211: {"labels": ["cat3", "cat4"]}, 212: {"labels": ["cat5", "cat6"]}},
        )
        self.assertEqual(fig.fig_args["labels"], ["cat1", "cat2"])
        self.assertEqual(fig.plot_args[0]["labels"], ["cat3", "cat4"])
        self.assertEqual(fig.plot_args[1]["labels"], ["cat5", "cat6"])

    def test_block_arranger(self):
        self.assertEqual(
            list(
                Waffle._block_arranger(
                    rows=2, columns=3, row_order=1, column_order=1, is_vertical=False, is_snake=False
                )
            ),
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
        )
        self.assertEqual(
            list(
                Waffle._block_arranger(
                    rows=2, columns=3, row_order=-1, column_order=1, is_vertical=True, is_snake=False
                )
            ),
            [(0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0)],
        )
        self.assertEqual(
            list(
                Waffle._block_arranger(rows=2, columns=3, row_order=-1, column_order=1, is_vertical=True, is_snake=True)
            ),
            [(0, 1), (1, 1), (2, 1), (2, 0), (1, 0), (0, 0)],
        )
        self.assertEqual(
            list(
                Waffle._block_arranger(rows=0, columns=0, row_order=1, column_order=1, is_vertical=True, is_snake=False)
            ),
            [],
        )

    def test_legend(self):
        fig = plt.figure(FigureClass=Waffle, rows=10, values=[10], labels=["cat1"])
        self.assertEqual(fig.gca().get_legend().texts[0]._text, "cat1")

    def test_plot(self):
        test_plots_folder = "test_plots/"

        # Most of the parameters
        plot_file_name = "title_and_legend.png"
        data = {"Democratic": 48, "Republican": 46, "Libertarian": 3}
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=data,
            colors=("#983D3D", "#232066", "#DCB732"),
            title={"label": "Vote Percentage in 2016 US Presidential Election", "loc": "left"},
            labels=[f"{k} ({v}%)" for k, v in data.items()],
            legend={"loc": "lower left", "bbox_to_anchor": (0, -0.4), "ncol": len(data), "framealpha": 0},
            starting_location="NW",
        )
        fig.savefig(test_plots_folder + plot_file_name, bbox_inches="tight", facecolor="#EEEEEE")
        self.assertTrue(os.path.exists(test_plots_folder + plot_file_name))

        # Test positions
        plot_file_name = "subplot_types.png"
        fig = plt.figure(
            FigureClass=Waffle,
            plots={
                311: {
                    "values": [10, 10, 10],
                },
                312: {
                    "values": [10, 10, 10],
                },
                (3, 1, 3): {
                    "values": [10, 10, 10],
                },
            },
            rows=5,
        )
        fig.savefig(test_plots_folder + plot_file_name, bbox_inches="tight")
        self.assertTrue(os.path.exists(test_plots_folder + plot_file_name))

    def test_make_waffle(self):
        test_plots_folder = "test_plots/"

        # Most of the parameters
        plot_file_name = "make_waffle_on_ax.png"
        fig, ax = plt.subplots()
        ax.set_aspect(aspect="equal")
        data = {"Democratic": 48, "Republican": 46, "Libertarian": 3}
        Waffle.make_waffle(
            ax=ax,
            rows=5,
            values=data,
            colors=("#983D3D", "#232066", "#DCB732"),
            title={"label": "Vote Percentage in 2016 US Presidential Election", "loc": "left"},
            labels=[f"{k} ({v}%)" for k, v in data.items()],
            legend={"loc": "lower left", "bbox_to_anchor": (0, -0.4), "ncol": len(data), "framealpha": 0},
            starting_location="NW",
        )
        fig.savefig(test_plots_folder + plot_file_name, bbox_inches="tight", facecolor="#EEEEEE")
        self.assertTrue(os.path.exists(test_plots_folder + plot_file_name))


if __name__ == "__main__":
    unittest.main()
