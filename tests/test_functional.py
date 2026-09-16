#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Tests for the top-level waffle_chart() function."""

import inspect
import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pywaffle import Waffle, waffle_chart


class TestWaffleChartFunction(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_returns_figure_and_axes(self):
        fig, ax = waffle_chart([48, 46, 6], rows=5)
        self.assertIsInstance(fig, Waffle)
        self.assertIs(ax, fig.axes[0])
        self.assertEqual(len(ax.patches), 100)

    def test_draws_into_an_existing_axes(self):
        parent, axes = plt.subplots(1, 2)
        fig, ax = waffle_chart({"Yes": 70, "No": 30}, rows=5, ax=axes[0])
        self.assertIs(fig, parent)
        self.assertIs(ax, axes[0])
        self.assertEqual([t.get_text() for t in ax.get_legend().get_texts()], ["Yes", "No"])
        # The sibling axes is untouched
        self.assertEqual(len(axes[1].patches), 0)

    def test_figure_arguments_are_forwarded(self):
        fig, _ = waffle_chart([10, 20], rows=5, figsize=(6, 3), dpi=150)
        self.assertEqual(list(fig.get_size_inches()), [6, 3])
        self.assertEqual(fig.dpi, 150)

    def test_figure_arguments_are_rejected_with_an_existing_axes(self):
        _, ax = plt.subplots()
        with self.assertRaisesRegex(TypeError, "figsize"):
            waffle_chart([10, 20], rows=5, ax=ax, figsize=(4, 4))

    def test_columns_can_be_given_positionally(self):
        _, ax = waffle_chart([10, 20], 5, 10)
        self.assertEqual(len(ax.patches), 50)

    def test_matches_the_figure_class_form(self):
        _, ax = waffle_chart([48, 46, 6], rows=5, columns=10, starting_location="NW")
        reference = plt.figure(
            FigureClass=Waffle,
            values=[48, 46, 6],
            rows=5,
            columns=10,
            starting_location="NW",
        )
        self.assertEqual(
            [(p.get_x(), p.get_y(), tuple(p.get_facecolor())) for p in ax.patches],
            [(p.get_x(), p.get_y(), tuple(p.get_facecolor())) for p in reference.axes[0].patches],
        )

    def test_icons_and_legend(self):
        _, ax = waffle_chart({"A": 10, "B": 20}, rows=5, icons="star", icon_legend=True)
        self.assertEqual(len(ax.texts), 30)
        self.assertEqual([t.get_text() for t in ax.get_legend().get_texts()], ["A", "B"])

    def test_validation_errors_still_surface(self):
        with self.assertRaisesRegex(ValueError, "negative"):
            waffle_chart([10, -5], rows=5)
        with self.assertRaisesRegex(ValueError, "At least one of rows and columns"):
            waffle_chart([10, 20])

    def test_default_legend_dict_is_not_shared_between_calls(self):
        _, first = waffle_chart([10, 20], rows=5, labels=["A", "B"])
        _, second = waffle_chart([30, 40], rows=5, labels=["C", "D"])
        self.assertEqual([t.get_text() for t in first.get_legend().get_texts()], ["A", "B"])
        self.assertEqual([t.get_text() for t in second.get_legend().get_texts()], ["C", "D"])

    def test_signature_is_explicit_rather_than_kwargs_only(self):
        # The point of this function is that the parameters are visible to IDEs and help()
        params = inspect.signature(waffle_chart).parameters
        for name in (
            "values",
            "rows",
            "columns",
            "ax",
            "colors",
            "labels",
            "icons",
            "icon_style",
            "cmap_name",
            "starting_location",
            "block_arranging_style",
        ):
            self.assertIn(name, params)
        self.assertEqual(params["cmap_name"].default, "Set2")
        self.assertEqual(params["starting_location"].default, "SW")


if __name__ == "__main__":
    unittest.main()


class TestModuleIsNotShadowed(unittest.TestCase):
    """The function must not take the name of the pywaffle.waffle module.

    Binding `waffle` on the package shadowed the submodule, so `pywaffle.waffle.Waffle` and
    `import pywaffle.waffle as m; m.Waffle` both raised
    `AttributeError: 'function' object has no attribute 'Waffle'`.
    """

    def test_pywaffle_waffle_is_the_module(self):
        import types

        import pywaffle

        self.assertIsInstance(pywaffle.waffle, types.ModuleType)

    def test_attribute_access_through_the_package_works(self):
        import pywaffle

        self.assertIs(pywaffle.waffle.Waffle, pywaffle.Waffle)

    def test_import_as_alias_works(self):
        import pywaffle.waffle as module

        self.assertTrue(hasattr(module, "Waffle"))

    def test_the_short_alias_is_available_from_its_own_module(self):
        from pywaffle.functional import waffle, waffle_chart

        self.assertIs(waffle, waffle_chart)

    def test_the_short_alias_is_not_exported_from_the_package(self):
        import pywaffle

        self.assertNotIn("waffle", pywaffle.__all__)
        self.assertIn("waffle_chart", pywaffle.__all__)
