# This script finds the path to fontawesome files, and creates necessary mappings and matplotlib handlers.
# They will only be called when fontawesome is used.

import inspect
import json
import pathlib
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


def fontawesome_package_path() -> pathlib.Path:
    """
    Path to the static asset directory of the installed fontawesomefree package.
    """
    import fontawesomefree

    package_path = pathlib.Path(inspect.getsourcefile(fontawesomefree))
    return package_path.parent / "static/fontawesomefree"


def font_file_finder() -> Dict[str, pathlib.Path]:
    font_otf_path = (fontawesome_package_path() / "otfs").glob("*.otf")
    return {
        style: path
        for path in font_otf_path
        for style, font_suffix in FA_STYLES.items()
        if font_suffix.lower() in path.name.lower()
    }


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
    def __init__(self, text, color, **kwargs):
        self.text = text
        self.color = color
        self.kwargs = kwargs


def LegendClassFactory(name, BaseClass=TextLegendBase):
    def __init__(self, text, color, **kwargs):
        BaseClass.__init__(self, text=text, color=color, **kwargs)

    return type(name, (BaseClass,), {"__init__": __init__})


legend_style_class_mapping = {style: LegendClassFactory(name=f"{style.capitalize()}TextLegend") for style in FA_STYLES}


class TextLegendHandler(HandlerBase):
    def __init__(self, font_file):
        super().__init__()
        self.font_file = font_file

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
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


fontawesome_files = font_file_finder()
icons = icon_mapping_builder()
legend_handler_style_mapping = {
    v: TextLegendHandler(font_file=fontawesome_files[k]) for k, v in legend_style_class_mapping.items()
}
