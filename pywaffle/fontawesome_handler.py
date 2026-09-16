# This script finds the path to fontawesome files, and creates necessary mappings and matplotlib handlers.
# They will only be called when fontawesome is used.

import inspect
import json
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


@lru_cache(maxsize=None)
def font_file_finder() -> Dict[str, pathlib.Path]:
    """Map each Font Awesome style to the .otf file that provides it."""
    font_otf_path = (fontawesome_package_path() / "otfs").glob("*.otf")
    return {
        style: path
        for path in font_otf_path
        for style, font_suffix in FA_STYLES.items()
        if font_suffix.lower() in path.name.lower()
    }


@lru_cache(maxsize=None)
def icon_mapping_builder() -> Dict[str, Dict[str, str]]:
    """
    Build the icon name to Unicode character mapping from the metadata shipped with the installed
    fontawesomefree package.

    Reading it at runtime keeps the mapping in sync with whichever Font Awesome version is installed.
    Generating it at install time does not work, because a wheel install never runs setup.py.
    """
    icons_json_path = fontawesome_package_path() / "metadata" / "icons.json"
    with open(icons_json_path, "r") as f:
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
