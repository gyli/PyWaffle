#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Regression tests for bugs fixed in 1.2.0. Each test names the behaviour that was wrong."""

import itertools
import unittest
import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from pywaffle.waffle import Waffle


class WaffleTestCase(unittest.TestCase):
    def tearDown(self):
        plt.close("all")


class TestSubplotLegend(WaffleTestCase):
    """Subplots shared the figure-level legend dict, so subplot 2 rendered subplot 1's labels."""

    def test_each_subplot_uses_its_own_labels(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            plots={
                211: {"values": [10, 20], "labels": ["A", "B"]},
                212: {"values": [30, 40], "labels": ["C", "D"]},
            },
        )
        rendered = [[t.get_text() for t in ax.get_legend().get_texts()] for ax in fig.axes]
        self.assertEqual(rendered, [["A", "B"], ["C", "D"]])

    def test_figure_level_legend_dict_is_not_mutated(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            plots={
                211: {"values": [10, 20], "labels": ["A", "B"]},
                212: {"values": [30, 40], "labels": ["C", "D"]},
            },
        )
        self.assertEqual(fig.fig_args["legend"], {})

    def test_user_supplied_handles_are_not_replaced(self):
        handles = [Patch(color="red", label="X"), Patch(color="blue", label="Y")]
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=[10, 20],
            labels=["A", "B"],
            legend={"handles": handles},
        )
        colors = [p.get_facecolor()[:3] for p in fig.plot_args[0]["legend"]["handles"]]
        self.assertEqual(colors, [(1.0, 0.0, 0.0), (0.0, 0.0, 1.0)])


class TestFontSizeIsDPIIndependent(WaffleTestCase):
    """The default size assumed 96 DPI, so icons were 2x too large at 200 DPI (GitHub #33)."""

    @staticmethod
    def _icon_size(dpi, **kwargs):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            columns=10,
            values=[10, 20, 20],
            dpi=dpi,
            figsize=(5, 3),
            **kwargs,
        )
        return fig.axes[0].texts[0].get_fontproperties().get_size_in_points()

    def test_icon_size_is_the_same_at_every_dpi(self):
        sizes = [self._icon_size(dpi, icons="star") for dpi in (72, 96, 100, 200)]
        for size in sizes[1:]:
            self.assertAlmostEqual(size, sizes[0], places=6)

    def test_character_size_is_the_same_at_every_dpi(self):
        sizes = [self._icon_size(dpi, characters="*") for dpi in (72, 100, 200)]
        for size in sizes[1:]:
            self.assertAlmostEqual(size, sizes[0], places=6)

    def test_explicit_font_size_is_respected(self):
        self.assertEqual(self._icon_size(200, icons="star", font_size=14), 14)


class TestFontAwesomeMapping(WaffleTestCase):
    """The shipped mapping was generated for FA 5.14 but used against FA 6 fonts."""

    def test_mapping_matches_the_installed_font_metadata(self):
        import json

        from pywaffle.fontawesome_handler import fontawesome_package_path, icons

        metadata = json.load(open(fontawesome_package_path() / "metadata/icons.json"))
        for name, meta in metadata.items():
            for style in meta["styles"]:
                if style in icons:
                    self.assertEqual(
                        icons[style][name],
                        chr(int(meta["unicode"], 16)),
                        f"{style}/{name} maps to the wrong character",
                    )

    def test_every_icon_in_the_metadata_is_resolvable(self):
        import json

        from pywaffle.fontawesome_handler import fontawesome_package_path, icons

        metadata = json.load(open(fontawesome_package_path() / "metadata/icons.json"))
        missing = [
            f"{style}/{name}"
            for name, meta in metadata.items()
            for style in meta["styles"]
            if style in icons and name not in icons[style]
        ]
        self.assertEqual(missing, [])

    def test_every_alias_resolves_to_the_icon_it_names(self):
        import json

        from pywaffle.fontawesome_handler import fontawesome_package_path, icons

        metadata = json.load(open(fontawesome_package_path() / "metadata/icons.json"))
        checked = 0
        for name, meta in metadata.items():
            character = chr(int(meta["unicode"], 16))
            for style in meta["styles"]:
                if style not in icons:
                    continue
                for alias in meta.get("aliases", {}).get("names", []):
                    with self.subTest(icon=f"{style}/{alias}"):
                        self.assertEqual(icons[style].get(alias), character, f"{style}/{alias} -> {name}")
                    checked += 1
        self.assertGreater(checked, 0, "the installed metadata carries no aliases to check")

    def test_an_alias_never_shadows_a_canonical_name(self):
        """The mapping is built in two passes so that an alias cannot overwrite a real icon name.

        No such collision exists in the shipped metadata, so asserting against the live mapping
        proves nothing about the ordering. Build it from metadata that does collide instead: "b"
        is a real icon, and "a" claims "b" among its alias names.
        """
        import json
        import tempfile
        from pathlib import Path
        from unittest import mock

        from pywaffle.fontawesome_handler import icon_mapping_builder

        metadata = {
            "a": {"unicode": "f001", "styles": ["solid"], "aliases": {"names": ["b", "c"]}},
            "b": {"unicode": "f002", "styles": ["solid"]},
        }
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory)
            (package / "metadata").mkdir()
            (package / "metadata" / "icons.json").write_text(json.dumps(metadata))
            with mock.patch(
                "pywaffle.fontawesome_handler.fontawesome_package_path",
                return_value=package,
            ):
                mapping = icon_mapping_builder()

        # The real icon keeps its name, rather than being replaced by the other icon's alias
        self.assertEqual(mapping["solid"]["b"], chr(0xF002))
        # An alias that collides with nothing still resolves
        self.assertEqual(mapping["solid"]["c"], chr(0xF001))
        self.assertEqual(mapping["solid"]["a"], chr(0xF001))


class TestColormaps(WaffleTestCase):
    """cmap_name reached for .colors, which only a ListedColormap has."""

    def test_continuous_colormap_yields_one_color_per_category(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20, 30], cmap_name="RdBu")
        colors = fig.plot_args[0]["colors"]
        self.assertEqual(len(colors), 3)
        self.assertEqual(len(set(colors)), 3)

    def test_single_category_continuous_colormap(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10], cmap_name="viridis")
        self.assertEqual(len(fig.plot_args[0]["colors"]), 1)

    def test_large_listed_colormaps_are_sampled_not_truncated(self):
        # viridis and friends are ListedColormaps with 256 entries, so taking the first few gives
        # colours differing by a fraction of a percent - five identical-looking dark purple blocks
        for name in ("viridis", "plasma", "magma", "inferno", "cividis"):
            with self.subTest(cmap_name=name):
                colors = Waffle._colors_from_cmap(name, 5)
                self.assertEqual(len(colors), 5)
                separations = [
                    max(abs(a[i] - b[i]) for i in range(3))
                    for a, b in itertools.combinations([c[:3] for c in colors], 2)
                ]
                # Any two categories differ by at least 10% on some channel
                self.assertGreater(min(separations), 0.1)

    def test_a_qualitative_colormap_is_still_used_in_order(self):
        # Set2 is a designed 8-colour palette; it must not be resampled
        import matplotlib.pyplot as pyplot

        palette = list(pyplot.get_cmap("Set2").colors)
        self.assertEqual(Waffle._colors_from_cmap("Set2", 3), palette[:3])

    def test_the_boundary_between_the_two_behaviours(self):
        # tab20 has exactly 20 entries and is the largest qualitative map matplotlib ships
        import matplotlib.pyplot as pyplot

        from pywaffle.waffle import QUALITATIVE_COLORMAP_MAX

        self.assertEqual(QUALITATIVE_COLORMAP_MAX, 20)
        self.assertEqual(pyplot.get_cmap("tab20").N, QUALITATIVE_COLORMAP_MAX)
        self.assertEqual(Waffle._colors_from_cmap("tab20", 3), list(pyplot.get_cmap("tab20").colors)[:3])

    def test_every_matplotlib_qualitative_map_takes_the_palette_path(self):
        import matplotlib.pyplot as pyplot

        for name in (
            "Pastel1",
            "Pastel2",
            "Paired",
            "Accent",
            "Dark2",
            "Set1",
            "Set2",
            "Set3",
            "tab10",
            "tab20",
            "tab20b",
            "tab20c",
        ):
            with self.subTest(cmap_name=name):
                palette = list(pyplot.get_cmap(name).colors)
                self.assertEqual(Waffle._colors_from_cmap(name, 3), palette[:3])

    def test_listed_colormap_output_is_unchanged(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20])
        self.assertEqual(
            fig.plot_args[0]["colors"],
            [
                (0.4, 0.7607843137254902, 0.6470588235294118),
                (0.9882352941176471, 0.5529411764705883, 0.3843137254901961),
            ],
        )

    def test_listed_colormap_repeats_when_there_are_more_categories_than_colors(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[1] * 10)
        colors = fig.plot_args[0]["colors"]
        self.assertEqual(len(colors), 10)
        # Set2 has 8 colors, so the 9th category wraps back to the 1st
        self.assertEqual(colors[8], colors[0])


class TestLayoutEngine(WaffleTestCase):
    """set_tight_layout has been deprecated since matplotlib 3.6."""

    def test_no_deprecation_warning_is_emitted(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            warnings.simplefilter("error", PendingDeprecationWarning)
            plt.figure(FigureClass=Waffle, rows=5, values=[10, 20])

    def test_tight_selects_the_matching_layout_engine(self):
        from matplotlib.layout_engine import TightLayoutEngine

        # None follows the figure.autolayout rcParam, which defaults to False
        expected = {True: TightLayoutEngine, False: None, None: None}
        for tight, engine in expected.items():
            with self.subTest(tight=tight):
                fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], tight=tight)
                if engine is None:
                    self.assertIsNone(fig.get_layout_engine())
                else:
                    self.assertIsInstance(fig.get_layout_engine(), engine)

    def test_tight_dict_is_passed_to_the_layout_engine(self):
        from matplotlib.layout_engine import TightLayoutEngine

        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], tight={"pad": 2})
        self.assertIsInstance(fig.get_layout_engine(), TightLayoutEngine)
        self.assertEqual(fig.get_layout_engine().get()["pad"], 2)


class TestParameterValidation(WaffleTestCase):
    """Bad input used to be ignored, or to surface as KeyError / AttributeError / ZeroDivisionError."""

    def _assert_rejects(self, message, **kwargs):
        kwargs.setdefault("values", [10, 20])
        kwargs.setdefault("rows", 5)
        with self.assertRaisesRegex(ValueError, message):
            plt.figure(FigureClass=Waffle, **kwargs)

    def test_negative_values(self):
        # Previously drawn as a silently wrong chart
        self._assert_rejects("negative", values=[10, -5])
        self._assert_rejects("negative", values=[10, -5], rows=None, columns=5)
        self._assert_rejects("negative", values=[10, -5], columns=5)

    def test_values_summing_to_zero(self):
        # Previously ZeroDivisionError
        self._assert_rejects("sum to zero", values=[0, 0], columns=5)

    def test_unknown_block_arranging_style(self):
        # Previously accepted and silently drawn as "normal"
        self._assert_rejects("block_arranging_style", block_arranging_style="snaek")

    def test_unknown_starting_location(self):
        # Previously KeyError
        self._assert_rejects("starting_location", starting_location="XX")

    def test_unknown_rounding_rule(self):
        self._assert_rejects("rounding_rule", rounding_rule="bogus")

    def test_non_string_rounding_rule(self):
        # Previously AttributeError
        self._assert_rejects("rounding_rule", rounding_rule=1)

    def test_unknown_icon_style(self):
        # Previously KeyError
        self._assert_rejects("icon_style", icons="star", icon_style="bogus")

    def test_icon_style_length_mismatch(self):
        # Previously not checked at all
        self._assert_rejects("icon_style", icons="star", icon_style=["solid"])

    def test_icon_style_list_is_case_insensitive(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=[10, 20],
            icons="star",
            icon_style=["Solid", "SOLID"],
        )
        self.assertEqual(fig.plot_args[0]["icon_style"], ["solid", "solid"])

    def test_enum_arguments_stay_case_and_whitespace_insensitive(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=[10, 20],
            starting_location=" nw ",
            rounding_rule=" CEIL ",
        )
        self.assertEqual(fig.plot_args[0]["starting_location"], "NW")
        self.assertEqual(fig.plot_args[0]["rounding_rule"], "ceil")

    def test_dict_values_produce_a_list_of_labels(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values={"a": 10, "b": 20})
        self.assertEqual(fig.plot_args[0]["labels"], ["a", "b"])


class TestBlockGeometry(WaffleTestCase):
    """The block-placement loop was previously untested; CHANGELOG records three bugs in it."""

    @staticmethod
    def _block_colors(**kwargs):
        fig = plt.figure(FigureClass=Waffle, **kwargs)
        return [tuple(p.get_facecolor()) for p in fig.axes[0].patches]

    @staticmethod
    def _block_positions(**kwargs):
        fig = plt.figure(FigureClass=Waffle, **kwargs)
        return [(round(p.get_x(), 6), round(p.get_y(), 6)) for p in fig.axes[0].patches]

    def test_block_count_matches_the_grid(self):
        self.assertEqual(len(self._block_colors(rows=5, columns=10, values=[48, 46, 6])), 50)

    def test_blocks_per_category(self):
        colors = self._block_colors(rows=5, columns=10, values=[48, 46, 6])
        counts = {c: colors.count(c) for c in set(colors)}
        # 48/46/6 of 100 scaled to 50 blocks, rounded to nearest
        self.assertEqual(sorted(counts.values()), [3, 23, 24])

    def test_zero_value_category_draws_no_block(self):
        # CHANGELOG v0.6.4: consecutive zeros produced an extra block
        colors = self._block_colors(rows=2, columns=5, values=[5, 0, 0, 5])
        self.assertEqual(len(set(colors)), 2)
        self.assertEqual(len(colors), 10)

    def test_snake_reverses_every_other_line(self):
        # Snake changes where each block lands, not which category it belongs to,
        # so the positions differ while the set of occupied cells is identical.
        normal = self._block_positions(rows=2, columns=5, values=[5, 5])
        snake = self._block_positions(rows=2, columns=5, values=[5, 5], block_arranging_style="snake")
        self.assertNotEqual(normal, snake)
        self.assertEqual(sorted(normal), sorted(snake))
        # The first line is untouched; the second is walked in reverse
        self.assertEqual(normal[:2], snake[:2])
        self.assertEqual(normal[2:4], snake[2:4][::-1])

    def test_each_starting_location_places_the_first_block_in_its_corner(self):
        corners = {}
        for location in ("NW", "SW", "NE", "SE"):
            fig = plt.figure(
                FigureClass=Waffle,
                rows=4,
                columns=4,
                values=[1, 15],
                starting_location=location,
            )
            first = fig.axes[0].patches[0]
            corners[location] = (round(first.get_x(), 6), round(first.get_y(), 6))

        self.assertEqual(len(set(corners.values())), 4)
        self.assertLess(corners["SW"][0], corners["SE"][0])
        self.assertLess(corners["NW"][0], corners["NE"][0])
        self.assertLess(corners["SW"][1], corners["NW"][1])
        self.assertLess(corners["SE"][1], corners["NE"][1])


class TestArrangement(WaffleTestCase):
    """Orientation and arranging styles, including the columns-only sizing path."""

    @staticmethod
    def _positions(**kwargs):
        fig = plt.figure(FigureClass=Waffle, **kwargs)
        return [(round(p.get_x(), 6), round(p.get_y(), 6)) for p in fig.axes[0].patches]

    def test_vertical_fills_down_a_column_before_moving_across(self):
        horizontal = self._positions(rows=2, columns=3, values=[3, 3])
        vertical = self._positions(rows=2, columns=3, values=[3, 3], vertical=True)
        self.assertNotEqual(horizontal, vertical)
        self.assertEqual(sorted(horizontal), sorted(vertical))

    def test_columns_only_derives_the_row_count(self):
        fig = plt.figure(FigureClass=Waffle, columns=5, values=[7, 3])
        self.assertEqual(fig.plot_args[0]["rows"], 2)

    def test_rows_only_derives_the_column_count(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 10])
        self.assertEqual(fig.plot_args[0]["columns"], 4)

    def test_new_line_starts_each_category_on_its_own_line(self):
        # CHANGELOG v0.6.2 recorded a wrong block count for this style
        fig = plt.figure(
            FigureClass=Waffle,
            rows=3,
            values=[2, 2],
            block_arranging_style="new-line",
        )
        # Each category is padded up to a whole line of 3, so 2 lines are needed
        self.assertEqual(fig.plot_args[0]["columns"], 2)
        # Only the 4 valued blocks are opaque; the padding is transparent
        opaque = [p for p in fig.axes[0].patches if p.get_facecolor()[3] > 0]
        self.assertEqual(len(opaque), 4)

    def test_new_line_vertical(self):
        fig = plt.figure(
            FigureClass=Waffle,
            columns=3,
            values=[2, 2],
            vertical=True,
            block_arranging_style="new-line",
        )
        self.assertEqual(fig.plot_args[0]["rows"], 2)

    def test_new_line_pads_short_categories_with_transparent_blocks(self):
        # Padding to a whole line is the only case that produces transparent blocks;
        # ordinary scaling fills every cell.
        fig = plt.figure(FigureClass=Waffle, rows=3, values=[2, 2], block_arranging_style="new-line")
        transparent = [p for p in fig.axes[0].patches if p.get_facecolor()[3] == 0]
        self.assertEqual(len(transparent), 2)

        fig = plt.figure(FigureClass=Waffle, rows=2, columns=5, values=[3, 3])
        self.assertEqual([p for p in fig.axes[0].patches if p.get_facecolor()[3] == 0], [])


class TestLegendAndTitle(WaffleTestCase):
    def test_icon_legend_uses_icon_handles(self):
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=[10, 20],
            labels=["A", "B"],
            icons="star",
            icon_legend=True,
        )
        self.assertIn("handler_map", fig.plot_args[0]["legend"])
        self.assertEqual([t.get_text() for t in fig.axes[0].get_legend().get_texts()], ["A", "B"])

    def test_title_is_applied(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10], title={"label": "Hello"})
        self.assertEqual(fig.axes[0].get_title(), "Hello")

    def test_labels_from_legend_dict_alone(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], legend={"labels": ["A", "B"]})
        self.assertEqual([t.get_text() for t in fig.axes[0].get_legend().get_texts()], ["A", "B"])


class TestErrorPaths(WaffleTestCase):
    def test_values_is_required(self):
        with self.assertRaisesRegex(ValueError, "values is required"):
            plt.figure(FigureClass=Waffle, rows=5, values=[])

    def test_rows_or_columns_is_required(self):
        with self.assertRaisesRegex(ValueError, "At least one of rows and columns"):
            plt.figure(FigureClass=Waffle, values=[10, 20])

    def test_colors_length_mismatch(self):
        with self.assertRaisesRegex(ValueError, "colors"):
            plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], colors=["red"])

    def test_labels_length_mismatch(self):
        with self.assertRaisesRegex(ValueError, "labels"):
            plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], labels=["A"])

    def test_icons_length_mismatch(self):
        with self.assertRaisesRegex(ValueError, "icons"):
            plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], icons=["star", "tree", "car"])

    def test_characters_length_mismatch(self):
        with self.assertRaisesRegex(ValueError, "characters"):
            plt.figure(FigureClass=Waffle, rows=5, values=[10, 20], characters=["a", "b", "c"])

    def test_invalid_subplot_position_type(self):
        with self.assertRaisesRegex(TypeError, "Subplot position"):
            plt.figure(FigureClass=Waffle, rows=5, plots={1.5: {"values": [10]}})

    def test_tuple_subplot_position(self):
        fig = plt.figure(FigureClass=Waffle, rows=5, plots={(1, 1, 1): {"values": [10, 20]}})
        self.assertEqual(len(fig.axes), 1)

    def test_icon_size_is_deprecated_in_favour_of_font_size(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            fig = plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="star", icon_size=20)
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught))
        self.assertEqual(fig.axes[0].texts[0].get_fontproperties().get_size_in_points(), 20)


class TestMakeWaffleOnAxes(WaffleTestCase):
    def test_draws_into_an_existing_axes(self):
        fig, ax = plt.subplots()
        Waffle.make_waffle(ax=ax, rows=5, columns=10, values={"a": 30, "b": 20})
        self.assertEqual(len(ax.patches), 50)
        self.assertEqual([t.get_text() for t in ax.get_legend().get_texts()], ["a", "b"])


if __name__ == "__main__":
    unittest.main()
