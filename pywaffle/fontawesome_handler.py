# This script finds the path to fontawesome files, and creates necessary mappings and matplotlib handlers.
# They will only be called when fontawesome is used.

import inspect
import json
import os
import pathlib
from functools import lru_cache
from collections import defaultdict
from typing import Dict

import matplotlib.font_manager as fm
from matplotlib.legend_handler import HandlerBase
from matplotlib.text import Text

FA_STYLES = {
    "brands": "Brands-Regular-400",
    "solid": "Free-Solid-900",
    "regular": "Free-Regular-400",
}


MISSING_FONT_AWESOME = (
    "Drawing with icons requires Font Awesome, which is an optional dependency of PyWaffle.\n"
    "Install it with:\n"
    "    pip install 'pywaffle[icons]'\n"
    "or, if you manage the font package yourself:\n"
    "    pip install fontawesomefree"
)


#: Environment variable naming a directory of Font Awesome .otf files to use instead of the
#: fontawesomefree package. Set it to use a system-provided Font Awesome.
FONT_DIRECTORY_VARIABLE = "PYWAFFLE_FONTAWESOME_DIR"

#: Where distributions put Font Awesome. Searched only when the environment variable is unset and
#: the fontawesomefree package is not installed.
SYSTEM_FONT_DIRECTORIES = (
    "/usr/share/fonts/fontawesome",  # Fedora, fontawesome-fonts
    "/usr/share/fonts/OTF",  # Arch, otf-font-awesome
    "/usr/share/fonts/opentype/font-awesome",  # Debian and Ubuntu
    "/usr/share/fonts/truetype/font-awesome",
    "/usr/local/share/fonts",  # manual installs
    "/opt/homebrew/share/fonts",  # Homebrew on Apple silicon
    "/usr/local/share/fonts/otf",
)


def fontawesome_package_path() -> pathlib.Path:
    """Path to the static asset directory of the installed fontawesomefree package.

    Raises ImportError with installation instructions when the optional font package is absent,
    rather than letting a bare ModuleNotFoundError surface from several frames down.
    """
    try:
        import fontawesomefree
    except ImportError as exc:
        raise ImportError(MISSING_FONT_AWESOME) from exc

    package_path = pathlib.Path(inspect.getsourcefile(fontawesomefree))
    return package_path.parent / "static/fontawesomefree"


def _styles_in(directory: pathlib.Path) -> Dict[str, pathlib.Path]:
    """Match the .otf files in one directory to the Font Awesome styles they provide.

    Distributions keep the upstream file names -- "Font Awesome 6 Free-Solid-900.otf" and the
    like -- so the same suffix match works for a system directory as for the Python package.
    """
    if not directory.is_dir():
        return {}
    return {
        style: path
        for path in sorted(directory.glob("*.otf"))
        for style, font_suffix in FA_STYLES.items()
        if font_suffix.lower() in path.name.lower()
    }


def font_directory_candidates():
    """Directories to search for Font Awesome, most specific first.

    An explicit setting wins, then the Python package, then the places distributions install it.
    Yields (path, is_package) so the caller can tell whether icons.json sits alongside.
    """
    override = os.environ.get(FONT_DIRECTORY_VARIABLE)
    if override:
        yield pathlib.Path(override), False

    try:
        yield fontawesome_package_path() / "otfs", True
    except ImportError:
        pass

    for directory in SYSTEM_FONT_DIRECTORIES:
        yield pathlib.Path(directory), False


@lru_cache(maxsize=None)
def font_file_finder() -> Dict[str, pathlib.Path]:
    """Map each Font Awesome style to the .otf file that provides it.

    Prefers an explicitly configured directory, then the fontawesomefree package, then the system
    font directories, so a distribution can supply the fonts without the Python package.
    """
    searched = []
    for directory, _ in font_directory_candidates():
        found = _styles_in(directory)
        if found:
            return found
        searched.append(str(directory))

    raise ImportError(
        MISSING_FONT_AWESOME
        + "\n\nNo Font Awesome .otf files were found in:\n    "
        + "\n    ".join(searched or ["(nowhere searched)"])
        + f"\n\nSet {FONT_DIRECTORY_VARIABLE} to a directory of Font Awesome .otf files to use "
        "a system copy."
    )


def _metadata_file() -> pathlib.Path:
    """Path to Font Awesome's icons.json, if whatever is providing the fonts also provides it.

    The Python package ships it. Distribution font packages generally do not -- they package
    fonts, not the web tooling -- so this can legitimately find nothing.
    """
    for directory, is_package in font_directory_candidates():
        if not _styles_in(directory):
            continue
        candidates = [directory.parent / "metadata" / "icons.json"] if is_package else []
        candidates += [directory / "icons.json", directory / "metadata" / "icons.json"]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        break
    return None


def _mapping_from_metadata(path: pathlib.Path) -> Dict[str, Dict[str, str]]:
    """Build the name to character mapping from Font Awesome's own metadata.

    This is the better source: it carries the aliases, which the fonts do not.
    """
    with open(path, "r") as f:
        icons_metadata = json.load(f)

    mapping: Dict[str, Dict[str, str]] = defaultdict(dict)

    # Canonical names first, so that an alias of one icon can never shadow the real name of another
    for icon_name, icon_meta in icons_metadata.items():
        character = chr(int(icon_meta["unicode"], 16))
        for style in icon_meta["styles"]:
            mapping[style][icon_name] = character

    for icon_name, icon_meta in icons_metadata.items():
        character = chr(int(icon_meta["unicode"], 16))
        for style in icon_meta["styles"]:
            for alias in icon_meta.get("aliases", {}).get("names", []):
                mapping[style].setdefault(alias, character)

    return dict(mapping)


def _mapping_from_fonts() -> Dict[str, Dict[str, str]]:
    """Build the name to character mapping out of the font files themselves.

    Font Awesome stores real icon names as glyph names, so the character map inverted gives every
    canonical name without any metadata file. Read through matplotlib's own FreeType binding, so
    this needs no dependency beyond matplotlib.

    Two differences from the metadata, both checked rather than assumed:

    * Aliases are absent. They exist only in icons.json, so ``adjust`` will not resolve while
      ``circle-half-stroke`` will.
    * Where a glyph has several code points -- Font Awesome maps both its private-use code point
      and the matching real Unicode one -- this may pick the other one. It renders the same glyph,
      because both code points map to it.
    """
    from matplotlib.ft2font import FT2Font

    mapping: Dict[str, Dict[str, str]] = defaultdict(dict)
    for style, path in font_file_finder().items():
        face = FT2Font(str(path))
        for code_point, glyph_index in face.get_charmap().items():
            name = face.get_glyph_name(glyph_index)
            if name:
                mapping[style].setdefault(name, chr(code_point))
    return dict(mapping)


@lru_cache(maxsize=None)
def icon_mapping_builder() -> Dict[str, Dict[str, str]]:
    """Map each style's icon names to the characters that draw them.

    Prefers Font Awesome's own metadata, which includes aliases. Falls back to reading the fonts,
    so a system Font Awesome works even though distributions ship fonts without icons.json.

    Built at runtime either way, so the names always match the fonts actually being drawn from.
    Generating it at install time did not work, because a wheel install never runs setup.py.
    """
    metadata = _metadata_file()
    return _mapping_from_metadata(metadata) if metadata else _mapping_from_fonts()


class TextLegendBase:
    """A legend entry that is a glyph rather than a colour swatch."""

    def __init__(self, text, color, **kwargs):
        self.text = text
        self.color = color
        self.kwargs = kwargs


def LegendClassFactory(name, BaseClass=TextLegendBase):
    """Build a legend handle class for one Font Awesome style.

    matplotlib dispatches legend handlers by handle type, so each style needs a distinct class for
    its own handler to be selected.
    """

    def __init__(self, text, color, **kwargs):
        BaseClass.__init__(self, text=text, color=color, **kwargs)

    return type(name, (BaseClass,), {"__init__": __init__})


legend_style_class_mapping = {style: LegendClassFactory(name=f"{style.capitalize()}TextLegend") for style in FA_STYLES}


class TextLegendHandler(HandlerBase):
    """Draw a legend entry as a glyph from a given font file."""

    def __init__(self, font_file):
        super().__init__()
        self.font_file = font_file

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        """Return the artists that draw one legend entry."""
        x = xdescent + width / 2.0
        y = ydescent + height / 2.0
        kwargs = {
            "horizontalalignment": "center",
            "verticalalignment": "center",
            "color": orig_handle.color,
            "fontproperties": fm.FontProperties(fname=self.font_file, size=fontsize),
        }
        kwargs.update(orig_handle.kwargs)
        annotation = Text(x, y, orig_handle.text, **kwargs)
        return [annotation]


@lru_cache(maxsize=None)
def _legend_handlers() -> Dict:
    """Map each legend handle class to a handler that draws it in the right font."""
    files = font_file_finder()
    return {v: TextLegendHandler(font_file=files[k]) for k, v in legend_style_class_mapping.items()}


#: Resolved on first use rather than at import, so that importing this module -- which
#: _parameter_validation does simply to read FA_STYLES -- does not require the optional font
#: package. Anything that actually needs a font raises ImportError with install instructions.
_LAZY = {
    "fontawesome_files": font_file_finder,
    "icons": icon_mapping_builder,
    "legend_handler_style_mapping": _legend_handlers,
}


def __getattr__(name: str):
    """Resolve the font-backed module attributes on first access (PEP 562)."""
    if name in _LAZY:
        value = _LAZY[name]()
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
