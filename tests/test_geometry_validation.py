#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Validation of the grid, block geometry, anchor, value element types, and the block-count cap."""

import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pywaffle.functional import waffle
from pywaffle.waffle import MAX_BLOCKS, Waffle


class ValidationMixin:
    """Shared helpers for the validation tests.

    A mixin rather than a TestCase subclass, so it is not collected as a test class of its own.
    """

    def tearDown(self):
        """Close every figure, so a long parameter sweep does not accumulate them."""
        plt.close("all")

    def _rejects(self, message, **kwargs):
        """Assert that the given arguments raise a ValueError matching message."""
        kwargs.setdefault("values", [10, 20])
        kwargs.setdefault("rows", 5)
        with self.assertRaisesRegex(ValueError, message):
            plt.figure(FigureClass=Waffle, **kwargs)


class TestGridDimensions(ValidationMixin, unittest.TestCase):
    """rows and columns must be positive whole numbers."""

    def test_negative_rows_used_to_draw_an_empty_chart(self):
        """rows=-5 gave columns=-6 and zero blocks, with no error at all."""
        # rows=-5 produced columns=-6 and zero blocks, with no error at all
        self._rejects("rows should be a positive integer", rows=-5)

    def test_zero_and_negative_are_rejected(self):
        """Zero and negative grid dimensions are refused for both rows and columns."""
        self._rejects("rows should be a positive integer", rows=0)
        self._rejects("columns should be a positive integer", rows=None, columns=0)
        self._rejects("columns should be a positive integer", rows=None, columns=-1)

    def test_non_integer_gives_a_named_error_not_a_typeerror(self):
        """A float or string dimension names the argument instead of failing in arithmetic."""
        self._rejects("rows should be a positive integer", rows=2.5)
        self._rejects("rows should be a positive integer", rows="5")

    def test_an_integral_float_is_accepted_and_normalized(self):
        """rows=5.0 is a reasonable thing to pass, and becomes int 5."""
        fig = plt.figure(FigureClass=Waffle, rows=5.0, values=[10, 20])
        self.assertEqual(fig.plot_args[0]["rows"], 5)
        self.assertIsInstance(fig.plot_args[0]["rows"], int)

    def test_neither_given_is_still_its_own_error(self):
        """Omitting both dimensions keeps its original, more specific message."""
        self._rejects("At least one of rows and columns", rows=None)


class TestBlockGeometry(ValidationMixin, unittest.TestCase):
    """The block shape and spacing arguments must describe a drawable block."""

    def test_block_aspect_ratio_must_be_positive(self):
        """Zero gave a degenerate axis; negative gave an inverted one, both silently."""
        # 0 produced a degenerate axis and a matplotlib singular-transform warning
        self._rejects("block_aspect_ratio should be a positive number", block_aspect_ratio=0)
        # -1 produced an inverted x axis and a nonsense chart, with no error
        self._rejects("block_aspect_ratio should be a positive number", block_aspect_ratio=-1)

    def test_block_aspect_ratio_must_be_a_number(self):
        """A non-numeric aspect ratio is refused by name."""
        self._rejects("block_aspect_ratio should be a positive number", block_aspect_ratio="x")

    def test_interval_ratios_may_not_be_negative(self):
        """A negative interval made blocks overlap rather than sit apart."""
        self._rejects("interval_ratio_x should be zero or a positive number", interval_ratio_x=-1)
        self._rejects("interval_ratio_y should be zero or a positive number", interval_ratio_y=-0.5)

    def test_zero_interval_is_valid(self):
        """Zero spacing is legitimate: it is how a continuous tiled grid is drawn."""
        fig = plt.figure(FigureClass=Waffle, rows=2, columns=2, values=[2, 2], interval_ratio_x=0, interval_ratio_y=0)
        self.assertEqual(len(fig.axes[0].patches), 4)


class TestPlotAnchor(ValidationMixin, unittest.TestCase):
    """plot_anchor must be one of the documented positions."""

    def test_unknown_anchor_is_rejected(self):
        """matplotlib's set_anchor accepts any string, so nothing else catches this."""
        # matplotlib's set_anchor accepts any string, so this silently misplaced the plot
        self._rejects("plot_anchor should be one of", plot_anchor="XX")

    def test_anchor_is_case_insensitive(self):
        """Lowercase anchors are normalized, like the other enum arguments."""
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], plot_anchor="c")
        self.assertEqual(fig.axes[0].get_anchor(), "C")

    def test_every_documented_anchor_is_accepted(self):
        """Every value the docstring lists is actually accepted."""
        for anchor in ("C", "SW", "S", "SE", "E", "NE", "N", "NW", "W"):
            with self.subTest(anchor=anchor):
                fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], plot_anchor=anchor)
                self.assertEqual(fig.axes[0].get_anchor(), anchor)


class TestValueTypes(ValidationMixin, unittest.TestCase):
    """values must be a container of real numbers."""

    def test_non_numeric_elements_are_rejected(self):
        """None or a string among the values names the argument rather than failing in a comparison."""
        self._rejects("values should contain only numbers", values=[None])
        self._rejects("values should contain only numbers", values=["5"])
        self._rejects("values should contain only numbers", values=[1, 2, None])

    def test_booleans_are_rejected(self):
        """bool subclasses int, so True would otherwise have counted as one block."""
        # bool is a subclass of int, so True would silently count as one block
        self._rejects("values should contain only numbers", values=[True, False])

    def test_a_scalar_is_rejected_with_a_useful_message(self):
        """A bare number says what values should be, rather than failing in len()."""
        self._rejects("values should be a list, tuple, dict or pandas Series", values=5)

    def test_a_string_is_rejected_rather_than_iterated_per_character(self):
        """A string is sized and iterable, so it would otherwise be read as one value per character."""
        self._rejects("values should be a list, tuple, dict or pandas Series", values="abc")

    def test_floats_and_ints_are_both_fine(self):
        """Mixed ints and floats remain valid values."""
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 2.5])
        self.assertTrue(fig.axes[0].patches)


class TestBlockCountCap(ValidationMixin, unittest.TestCase):
    """An unscaled value used to turn into minutes of drawing rather than an error."""

    def test_an_oversized_chart_is_refused_immediately(self):
        """An unscaled value is refused before drawing, rather than grinding for minutes."""
        # Refused before any drawing happens, so this returns instantly rather than grinding
        with self.assertRaisesRegex(ValueError, "over the limit"):
            plt.figure(FigureClass=Waffle, rows=2, values=[1e8])

    def test_the_message_says_how_to_fix_it(self):
        """The error names the block count and both ways out of it."""
        with self.assertRaises(ValueError) as caught:
            plt.figure(FigureClass=Waffle, rows=2, values=[1e8])
        message = str(caught.exception)
        self.assertIn("Pass both rows and columns", message)
        self.assertIn("MAX_BLOCKS", message)
        self.assertIn("100,000,000", message)

    def test_scaling_into_a_fixed_grid_is_the_way_out(self):
        """Giving both dimensions scales a huge value into a drawable chart."""
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[1e8])
        self.assertEqual(len(fig.axes[0].patches), 50)

    def test_only_above_the_limit_is_refused(self):
        """The comparison is strictly greater, so a grid of exactly MAX_BLOCKS is allowed."""
        # The comparison is strictly greater, so a grid of exactly MAX_BLOCKS is allowed
        self.assertEqual(MAX_BLOCKS, 10_000_000)
        with self.assertRaisesRegex(ValueError, "over the limit"):
            plt.figure(FigureClass=Waffle, rows=MAX_BLOCKS // 1000, columns=1001, values=[10, 20])

    def test_the_cap_is_overridable(self):
        """MAX_BLOCKS is a module constant so it can be raised or lowered."""
        import importlib

        module = importlib.import_module("pywaffle.waffle")
        original = module.MAX_BLOCKS
        try:
            module.MAX_BLOCKS = 10
            with self.assertRaisesRegex(ValueError, "over the limit"):
                plt.figure(FigureClass=Waffle, rows=5, columns=5, values=[10, 20])
        finally:
            module.MAX_BLOCKS = original


class TestValidationReachesTheFunctionAPI(ValidationMixin, unittest.TestCase):
    """Validation applies whichever entry point is used."""

    def test_waffle_function_validates_too(self):
        """Validation is not bypassed by the functional entry point."""
        with self.assertRaisesRegex(ValueError, "rows should be a positive integer"):
            waffle([10, 20], rows=-5)

    def test_make_waffle_validates_too(self):
        """Validation is not bypassed when drawing into an existing axes."""
        _, ax = plt.subplots()
        with self.assertRaisesRegex(ValueError, "plot_anchor should be one of"):
            Waffle.make_waffle(ax=ax, rows=5, values=[10, 20], plot_anchor="XX")


if __name__ == "__main__":
    unittest.main()
