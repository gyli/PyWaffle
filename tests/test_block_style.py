#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Tests for background_color, block_edge_color and block_edge_width (GitHub #37)."""

import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from pywaffle.waffle import Waffle


class BlockStyleTestCase(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    @staticmethod
    def _blocks(ax):
        return [p for p in ax.patches if p.get_zorder() != 0]

    @staticmethod
    def _background(ax):
        backgrounds = [p for p in ax.patches if p.get_zorder() == 0]
        return backgrounds[0] if backgrounds else None


class TestDefaultsAreUnchanged(BlockStyleTestCase):
    """Blocks have always been drawn with color=, which sets face and edge alike."""

    def test_face_and_edge_still_match_when_no_edge_is_given(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20])
        for block in self._blocks(fig.axes[0]):
            self.assertEqual(tuple(block.get_facecolor()), tuple(block.get_edgecolor()))

    def test_no_background_rectangle_by_default(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 20])
        self.assertIsNone(self._background(fig.axes[0]))
        self.assertEqual(len(fig.axes[0].patches), 50)

    def test_block_style_helper_passes_color_through_untouched(self):
        self.assertEqual(Waffle._block_style("red", None, None), {"color": "red"})


class TestBlockEdge(BlockStyleTestCase):
    def test_edge_color_is_applied_without_changing_the_face(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], colors=["red", "blue"], block_edge_color="white")
        blocks = self._blocks(fig.axes[0])
        self.assertEqual(tuple(blocks[0].get_facecolor()), to_rgba("red"))
        self.assertEqual(tuple(blocks[0].get_edgecolor()), to_rgba("white"))

    def test_edge_width_is_applied(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], block_edge_color="white", block_edge_width=2.5)
        self.assertEqual(self._blocks(fig.axes[0])[0].get_linewidth(), 2.5)

    def test_edge_width_alone_keeps_the_edge_the_face_color(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], colors=["red", "blue"], block_edge_width=3)
        block = self._blocks(fig.axes[0])[0]
        self.assertEqual(tuple(block.get_edgecolor()), to_rgba("red"))
        self.assertEqual(block.get_linewidth(), 3)

    def test_applies_to_fractional_blocks_too(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=[10.5, 20.25],
            rounding_rule="float",
            block_edge_color="white",
            block_edge_width=1.5,
        )
        blocks = self._blocks(fig.axes[0])
        self.assertTrue(blocks)
        for block in blocks:
            self.assertEqual(tuple(block.get_edgecolor()), to_rgba("white"))
            self.assertEqual(block.get_linewidth(), 1.5)

    def test_block_style_helper_separates_face_and_edge(self):
        self.assertEqual(
            Waffle._block_style("red", "white", 2),
            {"facecolor": "red", "edgecolor": "white", "linewidth": 2},
        )
        self.assertEqual(Waffle._block_style("red", "white", None), {"facecolor": "red", "edgecolor": "white"})


class TestNewLinePaddingHasNoEdge(BlockStyleTestCase):
    """block_arranging_style="new-line" pads a category out to a whole line with blank cells.

    They are drawn as fully transparent rectangles, which is invisible by default because a block
    takes face and edge from one colour. An edge argument sets the edge independently, so the
    padding came out as empty outlined squares after the end of the chart.
    """

    KWARGS = {"rows": 5, "values": [3, 3], "block_arranging_style": "new-line"}

    def _padding(self, **kwargs):
        fig = plt.figure(FigureClass=Waffle, **self.KWARGS, **kwargs)
        padding = [p for p in self._blocks(fig.axes[0]) if p.get_facecolor()[3] == 0]
        self.assertEqual(len(padding), 4, "expected two blank cells on each of the two lines")
        return padding

    def test_edge_color_does_not_outline_the_padding(self):
        for block in self._padding(block_edge_color="black", block_edge_width=2):
            self.assertEqual(block.get_edgecolor()[3], 0)

    def test_edge_width_alone_does_not_outline_the_padding(self):
        for block in self._padding(block_edge_width=3):
            self.assertEqual(block.get_edgecolor()[3], 0)

    def test_valued_blocks_still_get_their_edge(self):
        fig = plt.figure(FigureClass=Waffle, **self.KWARGS, block_edge_color="black")
        valued = [p for p in self._blocks(fig.axes[0]) if p.get_facecolor()[3] > 0]
        self.assertEqual(len(valued), 6)
        for block in valued:
            self.assertEqual(tuple(block.get_edgecolor()), to_rgba("black"))

    def test_the_padding_is_still_drawn_and_still_invisible(self):
        # Kept as artists so the block count is unchanged; just with nothing visible about them
        for kwargs in ({}, {"block_edge_color": "black"}):
            with self.subTest(**kwargs):
                fig = plt.figure(FigureClass=Waffle, **self.KWARGS, **kwargs)
                blocks = self._blocks(fig.axes[0])
                self.assertEqual(len(blocks), 10)
                for block in blocks:
                    if block.get_facecolor()[3] == 0:
                        self.assertEqual(block.get_edgecolor()[3], 0)


class TestBackgroundColor(BlockStyleTestCase):
    """The issue's actual request: fill the gaps between blocks."""

    def test_background_covers_the_grid_exactly(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 20], background_color="#dddddd")
        ax = fig.axes[0]
        background = self._background(ax)
        self.assertIsNotNone(background)
        self.assertEqual((background.get_x(), background.get_y()), (0, 0))
        self.assertAlmostEqual(background.get_width(), ax.get_xlim()[1], places=9)
        self.assertAlmostEqual(background.get_height(), ax.get_ylim()[1], places=9)

    def test_background_sits_behind_the_blocks(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 20], background_color="#dddddd")
        ax = fig.axes[0]
        self.assertEqual(self._background(ax).get_zorder(), 0)
        self.assertTrue(all(b.get_zorder() > 0 for b in self._blocks(ax)))

    def test_background_uses_the_given_color_and_no_edge(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 20], background_color="#2b2b2b")
        background = self._background(fig.axes[0])
        self.assertEqual(tuple(background.get_facecolor()), to_rgba("#2b2b2b"))
        self.assertEqual(background.get_edgecolor()[3], 0)

    def test_block_count_is_unaffected(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 20], background_color="#dddddd")
        self.assertEqual(len(self._blocks(fig.axes[0])), 50)

    def test_works_with_any_block_shape_and_spacing(self):
        # The reason a background rectangle was chosen over per-block edges
        fig = plt.figure(
            FigureClass=Waffle,
            rows=4,
            columns=8,
            values=[20, 12],
            block_aspect_ratio=2.5,
            interval_ratio_x=0.6,
            interval_ratio_y=0.1,
            background_color="#dddddd",
        )
        ax = fig.axes[0]
        background = self._background(ax)
        self.assertAlmostEqual(background.get_width(), ax.get_xlim()[1], places=9)

    def test_each_subplot_gets_its_own_background(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            plots={
                211: {"values": [10, 20], "background_color": "#ff0000"},
                212: {"values": [10, 20]},
            },
        )
        self.assertIsNotNone(self._background(fig.axes[0]))
        self.assertIsNone(self._background(fig.axes[1]))

    def test_combines_with_edges(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            columns=10,
            values=[30, 20],
            background_color="#2b2b2b",
            block_edge_color="white",
            block_edge_width=1,
        )
        ax = fig.axes[0]
        self.assertIsNotNone(self._background(ax))
        self.assertEqual(tuple(self._blocks(ax)[0].get_edgecolor()), to_rgba("white"))


class TestIconsAreUnaffected(BlockStyleTestCase):
    """Icons and characters draw Text artists, which have no block edge to colour."""

    def test_background_still_works_behind_icons(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], icons="star", background_color="#dddddd")
        self.assertIsNotNone(self._background(fig.axes[0]))
        self.assertEqual(len(fig.axes[0].texts), 30)

    def test_block_edge_is_silently_irrelevant_for_icons(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], icons="star", block_edge_color="white")
        self.assertEqual(len(fig.axes[0].texts), 30)
        self.assertEqual(self._blocks(fig.axes[0]), [])


if __name__ == "__main__":
    unittest.main()
