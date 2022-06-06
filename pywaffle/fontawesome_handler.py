# This script finds the path to fontawesome files, and creates necessary mappings and matplotlib handlers.
# They will only be called when fontawesome is used.

import inspect
import pathlib

import fontawesomefree
import matplotlib.font_manager as fm
from matplotlib.legend_handler import HandlerBase
from matplotlib.text import Text

FA_STYLES = (
    "brands",
    "solid",
    "regular",
)

package_path = pathlib.Path(inspect.getsourcefile(fontawesomefree))
font_otf_path = (package_path.parent / "static/fontawesomefree/otfs").glob("*.otf")

fontawesome_files = {
    style: f for f in font_otf_path for style in FA_STYLES if style in f.name.lower()
}


class TextLegendBase:
    def __init__(self, text, color, **kwargs):
        self.text = text
        self.color = color
        self.kwargs = kwargs


class SolidTextLegend(TextLegendBase):
    def __init__(self, text, color, **kwargs):
        super().__init__(text, color, **kwargs)


class RegularTextLegend(TextLegendBase):
    def __init__(self, text, color, **kwargs):
        super().__init__(text, color, **kwargs)


class BrandsTextLegend(TextLegendBase):
    def __init__(self, text, color, **kwargs):
        super().__init__(text, color, **kwargs)


legend_style_class_mapping = {
    "solid": SolidTextLegend,
    "regular": RegularTextLegend,
    "brands": BrandsTextLegend,
}


class TextLegendHandler(HandlerBase):
    def __init__(self, font_file):
        super().__init__()
        self.font_file = font_file

    def create_artists(
        self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans
    ):
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


legend_handler_style_mapping = {
    SolidTextLegend: TextLegendHandler(fontawesome_files["solid"]),
    RegularTextLegend: TextLegendHandler(fontawesome_files["regular"]),
    BrandsTextLegend: TextLegendHandler(fontawesome_files["brands"]),
}
