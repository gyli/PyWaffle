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
import sys
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
    handler.reload_font_awesome()


@unittest.skipIf(not HAS_FONT_AWESOME, "needs a Font Awesome to copy into a fake system directory")
class TestSystemFontDirectory(unittest.TestCase):
    """A directory of .otf files, with no metadata beside them."""

    @classmethod
    def setUpClass(cls):
        """Build a directory holding only fonts, the way a distribution package does."""
        cls.font_dir = pathlib.Path(tempfile.mkdtemp())
        reset_caches()
        for path in handler.font_file_finder().values():
            shutil.copy(path, cls.font_dir)
        reset_caches()

    @classmethod
    def tearDownClass(cls):
        # Clear the caches first, so nothing is still holding a font open. Windows refuses to
        # delete an open file, and FreeType keeps the handle for the life of the face object.
        reset_caches()
        shutil.rmtree(cls.font_dir, ignore_errors=True)

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
        self.assertEqual(pathlib.Path(candidates[0]), pathlib.Path("/nonexistent-on-purpose"))
        system = [pathlib.Path(d) for d in handler.SYSTEM_FONT_DIRECTORIES]
        self.assertTrue(any(pathlib.Path(c) in system for c in candidates))
        self.assertLess(candidates.index(candidates[0]), len(candidates) - 1)

    def test_the_package_is_flagged_as_the_package(self):
        """Only the package has icons.json one level up, so the caller has to be able to tell."""
        flags = [is_package for _, is_package in handler.font_directory_candidates()]
        self.assertEqual(flags.count(True), 1 if HAS_FONT_AWESOME else 0)


if __name__ == "__main__":
    unittest.main()


class TestExplicitDirectoryIsNotIgnored(unittest.TestCase):
    """An explicitly configured directory that yields nothing must say so.

    Falling through to the Python package would leave someone believing their system font was in
    use when it was not.
    """

    def setUp(self):
        self._saved = os.environ.get(handler.FONT_DIRECTORY_VARIABLE)
        self._tmp = pathlib.Path(tempfile.mkdtemp())
        reset_caches()

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        else:
            os.environ[handler.FONT_DIRECTORY_VARIABLE] = self._saved
        reset_caches()
        shutil.rmtree(self._tmp, ignore_errors=True)
        plt.close("all")

    def test_an_empty_directory_is_an_error(self):
        """Not a silent fallback to whatever else happens to be installed."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        with self.assertRaisesRegex(ImportError, "contains no Font Awesome"):
            handler.font_file_finder()

    def test_unrecognised_fonts_are_named(self):
        """Font Awesome 4 ships one FontAwesome.otf with no style split, and Fedora packages it."""
        (self._tmp / "FontAwesome.otf").write_bytes(b"not really a font")
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        with self.assertRaises(ImportError) as caught:
            handler.font_file_finder()
        message = str(caught.exception)
        self.assertIn("FontAwesome.otf", message)
        self.assertIn("Font Awesome 4 is not supported", message)

    def test_a_missing_directory_is_an_error(self):
        """A typo in the variable should not quietly do nothing."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp / "nope")
        with self.assertRaisesRegex(ImportError, "contains no Font Awesome"):
            handler.font_file_finder()


@unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome installed")
class TestUnknownIconNames(unittest.TestCase):
    """Which names exist depends on the installed Font Awesome version and on the style."""

    @staticmethod
    def tearDown():
        """Close the figures each test leaves behind."""
        plt.close("all")

    def test_an_icon_in_another_style_says_which(self):
        """bluesky is a brands icon, and the default style is solid."""
        with self.assertRaises(ValueError) as caught:
            plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="bluesky")
        message = str(caught.exception)
        self.assertIn("'brands'", message)
        self.assertIn("icon_style='brands'", message)

    def test_a_near_miss_is_suggested(self):
        """A typo should not read the same as an icon that does not exist."""
        with self.assertRaises(ValueError) as caught:
            plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="strr")
        self.assertIn("Did you mean", str(caught.exception))
        self.assertIn("'star'", str(caught.exception))

    def test_an_unknown_name_mentions_the_installed_version(self):
        """The usual cause is an icon added after the Font Awesome the user has."""
        with self.assertRaises(ValueError) as caught:
            plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="definitely-not-an-icon")
        message = str(caught.exception)
        self.assertIn("installed Font Awesome", message)
        self.assertIn("Font Awesome versions", message)

    def test_it_is_a_valueerror_like_every_other_argument_error(self):
        """A bare KeyError is not catchable alongside the rest of the argument validation."""
        with self.assertRaises(ValueError):
            plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="definitely-not-an-icon")


class TestFontAwesomeStatus(unittest.TestCase):
    """Which font is in use should never be a guess."""

    def setUp(self):
        self._saved = os.environ.get(handler.FONT_DIRECTORY_VARIABLE)
        self._tmp = pathlib.Path(tempfile.mkdtemp())
        reset_caches()

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        else:
            os.environ[handler.FONT_DIRECTORY_VARIABLE] = self._saved
        reset_caches()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_it_never_raises(self):
        """It is a diagnostic, so it has to work in exactly the situations that are broken."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp / "nowhere")
        status = handler.font_awesome_status()
        self.assertFalse(status.available)
        self.assertIsNotNone(status.problem)

    def test_a_failure_still_says_how_to_install(self):
        """The whole point of reporting a problem is telling the user what to do about it."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        self.assertIn("pip install 'pywaffle[icons]'", handler.font_awesome_status().problem)

    @unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome installed")
    def test_it_names_the_package_as_the_source(self):
        """The common case: the extra is installed and nothing is overridden."""
        os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        reset_caches()
        status = handler.font_awesome_status()
        self.assertTrue(status.available)
        self.assertEqual(status.source, "fontawesomefree package")
        self.assertTrue(status.aliases_available, "the package ships icons.json")
        self.assertRegex(status.version or "", r"^\d+\.")
        self.assertEqual(set(status.fonts), {"solid", "regular", "brands"})

    @unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome to copy")
    def test_it_names_an_overridden_directory_and_the_missing_aliases(self):
        """Someone using a system font needs to know the aliases are unavailable."""
        for path in handler.font_file_finder().values():
            shutil.copy(path, self._tmp)
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        reset_caches()
        status = handler.font_awesome_status()
        self.assertTrue(status.available)
        self.assertIn(handler.FONT_DIRECTORY_VARIABLE, status.source)
        self.assertEqual(status.directory, self._tmp)
        self.assertFalse(status.aliases_available, "no icons.json beside the fonts")
        self.assertEqual(status.version, "6", "major version read from the font family name")

    @unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome installed")
    def test_the_report_reads_as_a_report(self):
        """It is printed by people diagnosing a problem, so the text matters."""
        os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        reset_caches()
        text = str(handler.font_awesome_status())
        for expected in ("Font Awesome", "source:", "directory:", "aliases:", "solid"):
            self.assertIn(expected, text)

    def test_it_is_exported_from_the_package(self):
        """Discoverable as pywaffle.font_awesome_status, not buried in a submodule."""
        import pywaffle

        self.assertIn("font_awesome_status", pywaffle.__all__)
        self.assertIs(pywaffle.font_awesome_status, handler.font_awesome_status)


class TestHostileFontDirectories(unittest.TestCase):
    """PYWAFFLE_FONTAWESOME_DIR is user input, so nothing put in it may escape as a raw error.

    Every failure here should be ImportError or ValueError -- the two the rest of the package
    raises -- never OSError, RuntimeError or KeyError from somewhere deeper.
    """

    def setUp(self):
        self._saved = os.environ.get(handler.FONT_DIRECTORY_VARIABLE)
        self._tmp = pathlib.Path(tempfile.mkdtemp())
        reset_caches()

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        else:
            os.environ[handler.FONT_DIRECTORY_VARIABLE] = self._saved
        reset_caches()
        shutil.rmtree(self._tmp, ignore_errors=True)
        plt.close("all")

    def _draw(self):
        plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="star")

    def test_a_path_too_long_for_the_filesystem(self):
        """os.listdir raises OSError for these; it must not reach the caller."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = "/tmp/" + "a" * 300
        with self.assertRaises(ImportError):
            self._draw()

    def test_a_file_where_a_directory_was_expected(self):
        """Pointing at a font file rather than its directory is an easy mistake."""
        target = self._tmp / "afile"
        target.write_text("x")
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(target)
        with self.assertRaises(ImportError):
            self._draw()

    def test_a_blank_value_counts_as_unset(self):
        """An empty or whitespace variable should not be treated as a directory named ''."""
        for blank in ("", "   ", "\t"):
            with self.subTest(value=repr(blank)):
                os.environ[handler.FONT_DIRECTORY_VARIABLE] = blank
                reset_caches()
                self.assertIsNone(handler.configured_font_directory())

    def test_a_tilde_is_expanded(self):
        """A value set in code has not been through a shell."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = "~/some-fonts"
        self.assertEqual(handler.configured_font_directory(), pathlib.Path(os.path.expanduser("~/some-fonts")))

    def test_surrounding_whitespace_is_stripped(self):
        """Copy-pasted values often carry a trailing newline or space."""
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = f"  {self._tmp}  "
        self.assertEqual(handler.configured_font_directory(), self._tmp)

    @unittest.skipIf(not HAS_FONT_AWESOME, "needs a real font to sit beside the corrupt one")
    def test_a_file_that_is_not_really_a_font(self):
        """FreeType raises RuntimeError, which says nothing about which file was at fault."""
        for path in handler.font_file_finder().values():
            shutil.copy(path, self._tmp)
        # Truncate one of them, keeping the name that makes it a recognised style
        solid = next(p for p in self._tmp.glob("*.otf") if "Solid" in p.name)
        solid.write_bytes(b"not a font")
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        reset_caches()

        with self.assertRaises(ValueError) as caught:
            handler._mapping_from_fonts()
        self.assertIn(solid.name, str(caught.exception))

    def test_status_never_raises_whatever_the_variable_holds(self):
        """It is the tool people reach for when something is wrong."""
        for value in ("", "   ", "/tmp/" + "a" * 300, str(self._tmp), "~/nope", "relative/path"):
            with self.subTest(value=value[:30]):
                os.environ[handler.FONT_DIRECTORY_VARIABLE] = value
                reset_caches()
                status = handler.font_awesome_status()
                self.assertIsInstance(status.available, bool)
                self.assertIsInstance(str(status), str)


@unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome to build a partial set from")
class TestPartialFontSet(unittest.TestCase):
    """Distributions split the styles across packages, so having only some is normal.

    Fedora ships fontawesome-6-free-fonts and fontawesome-6-brands-fonts separately.
    """

    def setUp(self):
        self._saved = os.environ.get(handler.FONT_DIRECTORY_VARIABLE)
        self._tmp = pathlib.Path(tempfile.mkdtemp())
        reset_caches()
        solid = next(p for p in handler.font_file_finder().values() if "Solid" in p.name)
        shutil.copy(solid, self._tmp)
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        reset_caches()

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        else:
            os.environ[handler.FONT_DIRECTORY_VARIABLE] = self._saved
        reset_caches()
        shutil.rmtree(self._tmp, ignore_errors=True)
        plt.close("all")

    def test_the_available_style_still_works(self):
        """A partial set is not a broken set."""
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="star")
        self.assertEqual(len(fig.axes[0].texts), 10)

    def test_a_missing_style_says_which_styles_exist(self):
        """This used to be a bare KeyError naming only the style."""
        with self.assertRaises(ValueError) as caught:
            plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="bluesky", icon_style="brands")
        message = str(caught.exception)
        self.assertIn("'brands' is not available", message)
        self.assertIn("'solid'", message)
        self.assertIn("font_awesome_status", message)

    def test_a_missing_style_with_an_unknown_icon_also_explains_itself(self):
        """The style check has to come first, or the icon lookup raises KeyError on the style."""
        with self.assertRaises(ValueError) as caught:
            plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="nope", icon_style="regular")
        self.assertIn("not available", str(caught.exception))


class TestReloading(unittest.TestCase):
    """The fonts are resolved once, so changing the variable later needs an explicit reload."""

    def setUp(self):
        self._saved = os.environ.get(handler.FONT_DIRECTORY_VARIABLE)
        self._tmp = pathlib.Path(tempfile.mkdtemp())
        reset_caches()

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        else:
            os.environ[handler.FONT_DIRECTORY_VARIABLE] = self._saved
        reset_caches()
        shutil.rmtree(self._tmp, ignore_errors=True)
        plt.close("all")

    def test_it_is_exported(self):
        """Someone hitting the caching needs to be able to find the way out."""
        import pywaffle

        self.assertIn("reload_font_awesome", pywaffle.__all__)

    @unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome installed")
    def test_a_reload_picks_up_a_changed_directory(self):
        """Setting the variable in a notebook after drawing once should be recoverable."""
        os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        reset_caches()
        self.assertEqual(handler.font_awesome_status().source, "fontawesomefree package")

        for path in handler.font_file_finder().values():
            shutil.copy(path, self._tmp)
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)

        # Still the package: the resolution is cached
        self.assertEqual(handler.font_awesome_status().source, "fontawesomefree package")

        handler.reload_font_awesome()
        self.assertIn(str(self._tmp), handler.font_awesome_status().source)

    def test_reloading_with_nothing_resolved_yet_is_harmless(self):
        """It should be safe to call at any time, including before the first chart."""
        handler.reload_font_awesome()
        handler.reload_font_awesome()


class TestPlatformBehaviour(unittest.TestCase):
    """The search list has to be meaningful on the platform actually running.

    A Linux-only list makes the fallback silently useless on macOS and Windows, which looks
    identical to Font Awesome not being installed.
    """

    def test_the_directories_suit_this_platform(self):
        """Every entry should be somewhere this operating system could plausibly keep fonts."""
        directories = handler.SYSTEM_FONT_DIRECTORIES
        self.assertTrue(directories, "no system font directories for this platform")

        if sys.platform == "darwin":
            expected = "Library/Fonts"
        elif sys.platform == "win32":
            expected = "Fonts"
        else:
            expected = "/usr/share/fonts"
        self.assertTrue(
            any(expected in d for d in directories),
            f"no {expected!r} entry for {sys.platform}: {directories}",
        )

    @unittest.skipIf(sys.platform not in ("darwin", "win32"), "checks the non-Linux platforms")
    def test_linux_only_paths_are_not_the_whole_list(self):
        """The regression this guards: shipping only /usr/share/fonts everywhere."""
        non_linux = [d for d in handler.SYSTEM_FONT_DIRECTORIES if not d.startswith("/usr/share/fonts")]
        self.assertTrue(non_linux, "every entry is a Linux path on a non-Linux platform")

    def test_the_entries_are_absolute(self):
        """A relative entry would resolve against the working directory, which is nobody's fonts."""
        for directory in handler.SYSTEM_FONT_DIRECTORIES:
            with self.subTest(directory=directory):
                self.assertTrue(pathlib.Path(directory).is_absolute())

    def test_discovery_survives_directories_that_do_not_exist(self):
        """Most of the list will be absent on any given machine, which is normal."""
        candidates = list(handler.font_directory_candidates())
        self.assertTrue(candidates)
        # Must not raise merely from listing them
        for directory, _ in candidates:
            handler._styles_in(directory)


class TestFontFileNaming(unittest.TestCase):
    """Font file names vary in case between distributions and manual installs."""

    def setUp(self):
        self._saved = os.environ.get(handler.FONT_DIRECTORY_VARIABLE)
        self._tmp = pathlib.Path(tempfile.mkdtemp())
        reset_caches()

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(handler.FONT_DIRECTORY_VARIABLE, None)
        else:
            os.environ[handler.FONT_DIRECTORY_VARIABLE] = self._saved
        reset_caches()
        shutil.rmtree(self._tmp, ignore_errors=True)
        plt.close("all")

    @unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome to copy")
    def test_an_uppercase_extension_is_found(self):
        """glob("*.otf") is case sensitive whatever the filesystem, so .OTF was invisible."""
        source = next(p for p in handler.font_file_finder().values() if "Solid" in p.name)
        shutil.copy(source, self._tmp / (source.stem + ".OTF"))
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        reset_caches()

        self.assertIn("solid", handler.font_file_finder())
        fig = plt.figure(FigureClass=Waffle, rows=5, values=[10], icons="star")
        self.assertEqual(len(fig.axes[0].texts), 10)

    @unittest.skipIf(not HAS_FONT_AWESOME, "needs Font Awesome to copy")
    def test_the_style_suffix_match_ignores_case(self):
        """Some packagers lowercase the whole file name."""
        source = next(p for p in handler.font_file_finder().values() if "Solid" in p.name)
        shutil.copy(source, self._tmp / source.name.lower())
        os.environ[handler.FONT_DIRECTORY_VARIABLE] = str(self._tmp)
        reset_caches()
        self.assertIn("solid", handler.font_file_finder())

    def test_a_directory_of_unrelated_fonts_is_not_mistaken_for_font_awesome(self):
        """System font directories hold hundreds of fonts; only Font Awesome should match."""
        for name in ("Arial.otf", "DejaVuSans.otf", "SomeOther-Regular-400.otf"):
            (self._tmp / name).write_bytes(b"x")
        self.assertEqual(handler._styles_in(self._tmp), {})
