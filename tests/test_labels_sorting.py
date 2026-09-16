#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Tests for show_values, value_format, sort_values, and pandas Series input."""

import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pywaffle.waffle import Waffle


class LabelsTestCase(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    @staticmethod
    def _legend_texts(fig):
        return [t.get_text() for t in fig.axes[0].get_legend().get_texts()]


class TestShowValues(LabelsTestCase):
    """Replaces the f-string the documentation has always told people to write by hand."""

    DATA = {"Cat1": 10, "Cat2": 7, "Cat3": 9}

    def test_shows_the_raw_value(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, show_values=True)
        self.assertEqual(self._legend_texts(fig), ["Cat1 (10)", "Cat2 (7)", "Cat3 (9)"])

    def test_value_is_an_alias_for_true(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, show_values="value")
        self.assertEqual(self._legend_texts(fig), ["Cat1 (10)", "Cat2 (7)", "Cat3 (9)"])

    def test_shows_a_percentage_of_the_total(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, show_values="percentage")
        self.assertEqual(self._legend_texts(fig), ["Cat1 (38.5%)", "Cat2 (26.9%)", "Cat3 (34.6%)"])

    def test_value_format_overrides_the_number_formatting(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=self.DATA,
            show_values="percentage",
            value_format="{:.2f}%",
        )
        self.assertEqual(self._legend_texts(fig)[0], "Cat1 (38.46%)")

    def test_value_format_applies_to_raw_values_too(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, show_values=True, value_format="{:,.0f} units")
        self.assertEqual(self._legend_texts(fig)[0], "Cat1 (10 units)")

    def test_float_values_do_not_pick_up_trailing_zeros(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values={"A": 2.5, "B": 7.5}, show_values=True)
        self.assertEqual(self._legend_texts(fig), ["A (2.5)", "B (7.5)"])

    def test_works_with_an_icon_legend(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=self.DATA,
            icons="star",
            icon_legend=True,
            show_values="percentage",
        )
        self.assertEqual(self._legend_texts(fig)[0], "Cat1 (38.5%)")

    def test_off_by_default(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA)
        self.assertEqual(self._legend_texts(fig), ["Cat1", "Cat2", "Cat3"])

    def test_rejects_an_unknown_mode(self):
        with self.assertRaisesRegex(ValueError, "show_values"):
            plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, show_values="bogus")

    def test_percentage_of_a_zero_total_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "sum to more than zero"):
            plt.figure(FigureClass=Waffle, rows=5, values={"A": 0, "B": 0}, show_values="percentage")


class TestSortValues(LabelsTestCase):
    DATA = {"A": 5, "B": 20, "C": 10}

    def test_sorts_largest_first_by_default(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, sort_values=True)
        self.assertEqual(fig.plot_args[0]["values"], [20, 10, 5])
        self.assertEqual(fig.plot_args[0]["labels"], ["B", "C", "A"])

    def test_desc_is_an_alias_for_true(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, sort_values="desc")
        self.assertEqual(fig.plot_args[0]["values"], [20, 10, 5])

    def test_ascending(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, sort_values="asc")
        self.assertEqual(fig.plot_args[0]["values"], [5, 10, 20])
        self.assertEqual(fig.plot_args[0]["labels"], ["A", "C", "B"])

    def test_colors_move_with_their_category(self):
        # The whole hazard of sorting: a category keeping someone else's colour
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=self.DATA,
            colors=["red", "green", "blue"],
            sort_values=True,
        )
        self.assertEqual(fig.plot_args[0]["labels"], ["B", "C", "A"])
        self.assertEqual(fig.plot_args[0]["colors"], ["green", "blue", "red"])

    def test_icons_move_with_their_category(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values={"A": 5, "B": 20}, icons=["star", "tree"], sort_values=True)
        self.assertEqual(fig.plot_args[0]["labels"], ["B", "A"])
        # tree belonged to B, which now sorts first
        self.assertEqual([hex(ord(c)) for c in fig.plot_args[0]["icons"]], ["0xf1bb", "0xf005"])

    def test_icon_style_moves_with_its_category(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values={"A": 5, "B": 20},
            icons=["star", "star"],
            icon_style=["regular", "solid"],
            sort_values=True,
        )
        self.assertEqual(fig.plot_args[0]["icon_style"], ["solid", "regular"])

    def test_characters_move_with_their_category(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values={"A": 5, "B": 20}, characters=["x", "o"], sort_values=True)
        self.assertEqual(fig.plot_args[0]["characters"], ["o", "x"])

    def test_a_single_icon_string_is_left_alone(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA, icons="star", sort_values=True)
        self.assertEqual(len(set(fig.plot_args[0]["icons"])), 1)

    def test_off_by_default(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=self.DATA)
        self.assertEqual(fig.plot_args[0]["values"], [5, 20, 10])

    def test_block_counts_follow_the_sorted_order(self):
        fig = plt.figure(FigureClass=Waffle, rows=1, columns=7, values={"A": 5, "B": 20, "C": 10}, sort_values=True)
        colors = [tuple(p.get_facecolor()) for p in fig.axes[0].patches]
        # Largest category first, so its colour occupies the run of blocks from the start
        self.assertEqual(colors[0], tuple(fig.plot_args[0]["colors"][0]) + (1,))


class TestPandasInput(LabelsTestCase):
    def setUp(self):
        self.pd = __import__("pandas")

    def test_series_index_becomes_the_labels(self):
        series = self.pd.Series({"Alpha": 10, "Beta": 20, "Gamma": 5})
        fig = plt.figure(FigureClass=Waffle, rows=5, values=series)
        self.assertEqual(fig.plot_args[0]["labels"], ["Alpha", "Beta", "Gamma"])
        self.assertEqual(self._legend_texts(fig), ["Alpha", "Beta", "Gamma"])

    def test_dataframe_column_works_the_same_way(self):
        frame = self.pd.DataFrame({"n": [10, 20, 5]}, index=["A", "B", "C"])
        fig = plt.figure(FigureClass=Waffle, rows=5, values=frame["n"])
        self.assertEqual(fig.plot_args[0]["labels"], ["A", "B", "C"])

    def test_explicit_labels_still_win(self):
        series = self.pd.Series({"Alpha": 10, "Beta": 20})
        fig = plt.figure(FigureClass=Waffle, rows=5, values=series, labels=["One", "Two"])
        self.assertEqual(fig.plot_args[0]["labels"], ["One", "Two"])

    def test_values_become_a_plain_list(self):
        series = self.pd.Series({"Alpha": 10, "Beta": 20})
        fig = plt.figure(FigureClass=Waffle, rows=5, values=series)
        self.assertEqual(fig.plot_args[0]["values"], [10, 20])

    def test_a_non_string_index_is_still_usable(self):
        series = self.pd.Series([10, 20], index=[2021, 2022])
        fig = plt.figure(FigureClass=Waffle, rows=5, values=series)
        self.assertEqual(fig.plot_args[0]["labels"], ["2021", "2022"])

    def test_series_combines_with_sorting_and_values(self):
        series = self.pd.Series({"Alpha": 10, "Beta": 20, "Gamma": 5})
        fig = plt.figure(FigureClass=Waffle, rows=5, values=series, sort_values=True, show_values=True)
        self.assertEqual(self._legend_texts(fig), ["Beta (20)", "Alpha (10)", "Gamma (5)"])

    def test_a_plain_list_is_unaffected(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20])
        self.assertIsNone(fig.plot_args[0]["labels"])


class TestNormalizationIsAlreadySupported(LabelsTestCase):
    """Giving both rows and columns already scales arbitrary values to fill the grid."""

    def test_arbitrary_values_fill_the_grid_exactly(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[3, 7, 13])
        self.assertEqual(len(fig.axes[0].patches), 50)

    def test_proportions_are_preserved(self):
        fig = plt.figure(FigureClass=Waffle, rows=10, columns=10, values=[25, 25, 50])
        colors = [tuple(p.get_facecolor()) for p in fig.axes[0].patches]
        counts = sorted(colors.count(c) for c in set(colors))
        self.assertEqual(counts, [25, 25, 50])


if __name__ == "__main__":
    unittest.main()
