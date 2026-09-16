#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Tests for rounding_rule="float", which draws partially filled blocks (GitHub #26)."""

import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pywaffle.waffle import Waffle


class FractionalTestCase(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    @staticmethod
    def _block_size(plot_args):
        rows = plot_args["rows"]
        height = 1 / (rows + rows * plot_args["interval_ratio_y"] - plot_args["interval_ratio_y"])
        return plot_args["block_aspect_ratio"] * height, height

    def _drawn_area(self, fig):
        """Total coloured area, measured in whole blocks."""
        width, height = self._block_size(fig.plot_args[0])
        return sum(p.get_width() * p.get_height() for p in fig.axes[0].patches) / (width * height)


class TestAreaIsProportionalToValues(FractionalTestCase):
    """The point of the feature: no value is lost to rounding."""

    def test_area_equals_the_sum_of_values(self):
        for values in ([3.5, 2.5], [1.2, 86.26], [18.46, 1.64, 7.52, 15.3, 44.54], [7.25]):
            with self.subTest(values=values):
                fig = plt.figure(FigureClass=Waffle, values=values, rows=5, rounding_rule="float")
                self.assertAlmostEqual(self._drawn_area(fig), sum(values), places=6)

    def test_area_is_preserved_for_every_arranging_style(self):
        values = [18.46, 1.64, 7.52, 15.3, 44.54]
        for style in ("normal", "snake"):
            for vertical in (False, True):
                with self.subTest(style=style, vertical=vertical):
                    fig = plt.figure(
                        FigureClass=Waffle,
                        values=values,
                        rows=5,
                        rounding_rule="float",
                        block_arranging_style=style,
                        vertical=vertical,
                    )
                    self.assertAlmostEqual(self._drawn_area(fig), sum(values), places=6)

    def test_area_is_preserved_for_every_starting_location(self):
        for location in ("NW", "SW", "NE", "SE"):
            with self.subTest(location=location):
                fig = plt.figure(
                    FigureClass=Waffle,
                    values=[3.3, 4.7],
                    rows=3,
                    rounding_rule="float",
                    starting_location=location,
                )
                self.assertAlmostEqual(self._drawn_area(fig), 8, places=6)

    def test_both_dimensions_given_fills_the_grid_exactly(self):
        fig = plt.figure(FigureClass=Waffle, values=[1.2, 86.26], rows=5, columns=10, rounding_rule="float")
        self.assertAlmostEqual(self._drawn_area(fig), 50, places=6)

    def test_a_zero_value_contributes_nothing(self):
        fig = plt.figure(FigureClass=Waffle, values=[2.5, 0, 3.5], rows=3, rounding_rule="float")
        self.assertAlmostEqual(self._drawn_area(fig), 6, places=6)
        colors = {tuple(p.get_facecolor()) for p in fig.axes[0].patches}
        self.assertEqual(len(colors), 2)


class TestChartSizeIsStable(FractionalTestCase):
    """GitHub #26: two datasets with the same total produced charts of different sizes."""

    def test_equal_totals_produce_equal_chart_sizes(self):
        plot1 = {"Net income": 18.46, "Income tax": 1.64, "MG&A": 7.52, "R&D": 15.3, "Cost of sales": 44.54}
        plot2 = {"Misc income": 1.2, "Revenue": 86.26}
        self.assertAlmostEqual(sum(plot1.values()), sum(plot2.values()), places=9)

        sizes = [
            plt.figure(FigureClass=Waffle, values=data, rows=5, rounding_rule="float").plot_args[0]["columns"]
            for data in (plot1, plot2)
        ]
        self.assertEqual(sizes[0], sizes[1])

    def test_column_count_follows_the_total_only(self):
        # However the same total is split up, the grid is the same size
        for values in ([10.0], [5.0, 5.0], [3.3, 3.3, 3.4], [1.0] * 10):
            with self.subTest(values=values):
                fig = plt.figure(FigureClass=Waffle, values=values, rows=2, rounding_rule="float")
                self.assertEqual(fig.plot_args[0]["columns"], 5)


class TestSplitBlocks(FractionalTestCase):
    """A category boundary inside a block is drawn as two abutting rectangles."""

    def test_boundary_block_is_split_between_two_categories(self):
        fig = plt.figure(FigureClass=Waffle, values=[2.5, 2.5], rows=1, rounding_rule="float")
        width, _ = self._block_size(fig.plot_args[0])
        patches = fig.axes[0].patches

        # 5 cells, the middle one split in two
        self.assertEqual(len(patches), 6)
        halves = [p for p in patches if abs(p.get_width() - width / 2) < 1e-9]
        self.assertEqual(len(halves), 2)
        # The two halves share a cell and abut exactly
        self.assertAlmostEqual(halves[0].get_y(), halves[1].get_y())
        self.assertAlmostEqual(halves[0].get_x() + halves[0].get_width(), halves[1].get_x())
        self.assertNotEqual(halves[0].get_facecolor(), halves[1].get_facecolor())

    def test_split_runs_along_the_direction_of_travel(self):
        # With several rows the sequence runs up a column, so a split block is cut horizontally
        fig = plt.figure(FigureClass=Waffle, values=[2.5, 2.5], rows=5, rounding_rule="float")
        _, height = self._block_size(fig.plot_args[0])
        halves = [p for p in fig.axes[0].patches if abs(p.get_height() - height / 2) < 1e-9]
        self.assertEqual(len(halves), 2)

        # With a single row it runs along the columns, so the cut is vertical
        fig = plt.figure(FigureClass=Waffle, values=[2.5, 2.5], rows=1, rounding_rule="float")
        width, _ = self._block_size(fig.plot_args[0])
        halves = [p for p in fig.axes[0].patches if abs(p.get_width() - width / 2) < 1e-9]
        self.assertEqual(len(halves), 2)

    def test_partial_block_fills_from_the_side_the_sequence_arrives_at(self):
        expected_side = {"SW": "left", "NW": "left", "SE": "right", "NE": "right"}
        for location, side in expected_side.items():
            with self.subTest(location=location):
                fig = plt.figure(
                    FigureClass=Waffle,
                    values=[1.5, 2.5],
                    rows=1,
                    rounding_rule="float",
                    starting_location=location,
                )
                width, _ = self._block_size(fig.plot_args[0])
                first_color = fig.plot_args[0]["colors"][0]
                partial = [
                    p
                    for p in fig.axes[0].patches
                    if tuple(p.get_facecolor()[:3]) == tuple(first_color[:3]) and abs(p.get_width() - width) > 1e-9
                ]
                self.assertEqual(len(partial), 1)

                cell_pitch = (1 + fig.plot_args[0]["interval_ratio_x"]) * width
                offset = partial[0].get_x() - round(partial[0].get_x() / cell_pitch) * cell_pitch
                if side == "left":
                    self.assertAlmostEqual(offset, 0, places=6)
                else:
                    self.assertAlmostEqual(offset, width / 2, places=6)


class TestFractionalValidation(FractionalTestCase):
    def test_float_is_rejected_with_icons(self):
        with self.assertRaisesRegex(ValueError, "cannot be combined with icons or characters"):
            plt.figure(FigureClass=Waffle, values=[2.5, 2.5], rows=5, rounding_rule="float", icons="star")

    def test_float_is_rejected_with_characters(self):
        with self.assertRaisesRegex(ValueError, "cannot be combined with icons or characters"):
            plt.figure(FigureClass=Waffle, values=[2.5, 2.5], rows=5, rounding_rule="float", characters="*")

    def test_integer_rounding_rules_are_unchanged(self):
        for rule in ("nearest", "ceil", "floor"):
            with self.subTest(rule=rule):
                fig = plt.figure(FigureClass=Waffle, values=[3.4, 2.6], rows=2, rounding_rule=rule)
                width, height = self._block_size(fig.plot_args[0])
                for patch in fig.axes[0].patches:
                    self.assertAlmostEqual(patch.get_width(), width, places=9)
                    self.assertAlmostEqual(patch.get_height(), height, places=9)


class TestFractionalHelpers(FractionalTestCase):
    def test_coloured_spans_are_contiguous_without_padding(self):
        self.assertEqual(
            Waffle._coloured_spans([2.5, 3.5], [2.5, 3.5]),
            [(0, 0.0, 2.5), (1, 2.5, 6.0)],
        )

    def test_coloured_spans_leave_gaps_for_new_line_padding(self):
        # A category padded out to a whole line colours only part of its span
        self.assertEqual(
            Waffle._coloured_spans([4, 4], [2.5, 3.5]),
            [(0, 0.0, 2.5), (1, 4.0, 7.5)],
        )

    def test_cell_segments_splits_a_boundary_cell(self):
        spans = [(0, 0.0, 2.5), (1, 2.5, 6.0)]
        self.assertEqual(Waffle._cell_segments(spans, 0), [(0, 0.0, 1.0)])
        self.assertEqual(Waffle._cell_segments(spans, 2), [(0, 0.0, 0.5), (1, 0.5, 1.0)])
        self.assertEqual(Waffle._cell_segments(spans, 5), [(1, 0.0, 1.0)])

    def test_cell_segments_ignores_a_zero_width_touch(self):
        # A boundary landing exactly on a cell edge must not emit an empty sliver
        self.assertEqual(Waffle._cell_segments([(0, 0.0, 2.0), (1, 2.0, 4.0)], 1), [(0, 0.0, 1.0)])

    def test_fill_steps_follow_a_snake(self):
        cells = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.assertEqual(
            Waffle._fill_steps(cells, default_axis=1),
            [(1, 1), (1, 1), (1, -1), (1, -1)],
        )


if __name__ == "__main__":
    unittest.main()
