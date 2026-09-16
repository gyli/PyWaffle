#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Font Awesome supplied by the system rather than by the Python package.

Distributions package Font Awesome as fonts -- Fedora's fontawesome-6-free-fonts, Arch's
otf-font-awesome, Debian's fonts-font-awesome -- without the icons.json that the Python package
ships. So the names have to be recoverable from the fonts alone.
"""

import importlib.util
import os
import pathlib
import shutil
import tempfile
import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pywaffle import fontawesome_handler as handler
from pywaffle.waffle import Waffle

HAS_FONT_AWESOME = importlib.util.find_spec("fontawesomefree") is not None


def reset_caches():
    """Clear the resolved fonts and mapping, which are cached for the life of the process."""
    handler.font_file_finder.cache_clear()
    handler.icon_mapping_builder.cache_clear()
    for name in handler._LAZY:
        handler.__dict__.pop(name, None)


@unittest.skipIf(not HAS_FONT_AWESOME, "needs a Font Awesome to copy into a fake system directory")
class TestSystemFontDirectory(unittest.TestCase):
    """A directory of .otf files, with no metadata beside them."""

    @classmethod
    def setUpClass(cls):
        """Build a directory holding only fonts, the way a distribution package does."""
        cls._tmp = tempfile.TemporaryDirectory()
        cls.font_dir = pathlib.Path(cls._tmp.name)
        reset_caches()
        for path in handler.font_file_finder().values():
            shutil.copy(path, cls.font_dir)
        reset_caches()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()
        reset_caches()

    def setUp(self):
        self._saved = os.environ.get(handler.FONT_DIRECTORY_VARIABLE)
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self.font_dir)
        reset_caches()

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        else:
            os.environ[handler.FONT_DIRECTORY_VARIABLE] = self._saved
        reset_caches()
        plt.close("all")

    def test_the_override_is_used(self):
        """The environment variable beats the installed package."""
        for path in handler.font_file_finder().values():
            self.assertEqual(path.parent, self.font_dir)

    def test_no_metadata_is_found_beside_the_fonts(self):
        """The premise of this whole test case: distributions ship fonts without icons.json."""
        self.assertIsNone(handler._metadata_file())

    def test_names_are_recovered_from_the_fonts(self):
        """Font Awesome stores real icon names as glyph names, so the fonts alone are enough."""
        mapping = handler.icon_mapping_builder()
        self.assertEqual(set(mapping), {"solid", "regular", "brands"})
        for name in ("star", "heart", "car-side", "bicycle"):
            self.assertIn(name, mapping["solid"], f"{name} should be recoverable from the font")
        self.assertIn("bluesky", mapping["brands"])

    def test_icons_draw(self):
        """The point of the exercise."""
        fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 20], icons="star")
        self.assertEqual(len(fig.axes[0].texts), 50)

    def test_every_canonical_name_survives(self):
        """Only aliases are lost; no real icon name should be missing."""
        from_fonts = handler._mapping_from_fonts()
        os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        reset_caches()
        from_metadata = handler.icon_mapping_builder()

        import json

        metadata = json.load(open(handler._metadata_file()))
        for style in ("solid", "brands", "regular"):
            canonical = {n for n, m in metadata.items() if style in m["styles"]}
            missing = canonical - set(from_fonts[style])
            with self.subTest(style=style):
                self.assertEqual(sorted(missing), [], f"{len(missing)} canonical names lost")
            self.assertLess(len(from_fonts[style]), len(from_metadata[style]) + 400)

    def test_rendering_matches_the_packaged_fonts(self):
        """A chart drawn from system fonts must be the same chart.

        Some names resolve to a different code point -- Font Awesome maps both a private-use and a
        real Unicode code point to the same glyph -- so this compares what is drawn, not the
        characters chosen.
        """

        def positions_and_glyph_widths():
            fig = plt.figure(
                FigureClass=Waffle,
                rows=5,
                columns=10,
                values=[30, 12, 8],
                icons=["star", "car-side", "bicycle"],
                figsize=(6, 3),
                dpi=100,
            )
            fig.canvas.draw()
            out = [
                (round(t.get_position()[0], 6), round(t.get_position()[1], 6), round(t.get_window_extent().width, 4))
                for t in fig.axes[0].texts
            ]
            plt.close(fig)
            return out

        from_system = positions_and_glyph_widths()
        os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        reset_caches()
        from_package = positions_and_glyph_widths()

        self.assertEqual(from_system, from_package)


class TestDiscoveryOrder(unittest.TestCase):
    """Where PyWaffle looks, and in what order."""

    @staticmethod
    def tearDown():
        """Restore the caches other tests rely on."""
        reset_caches()

    def test_system_directories_are_searched_last(self):
        """An explicit setting beats the package, which beats the system."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = "/nonexistent-on-purpose"
        try:
            candidates = [str(d) for d, _ in handler.font_directory_candidates()]
        finally:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        self.assertEqual(candidates[0], "/nonexistent-on-purpose")
        self.assertTrue(any("/usr/share/fonts" in c for c in candidates))
        self.assertLess(candidates.index("/nonexistent-on-purpose"), len(candidates) - 1)

    def test_the_package_is_flagged_as_the_package(self):
        """Only the package has icons.json one level up, so the caller has to be able to tell."""
        flags = [is_package for _, is_package in handler.font_directory_candidates()]
        self.assertEqual(flags.count(True), 1 if HAS_FONT_AWESOME else 0)


if __name__ == "__main__":
    unittest.main()
