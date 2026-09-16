#!/usr/bin/python
# -*-coding: utf-8 -*-

import copy
import math
import numbers
import operator
from itertools import islice, product
from typing import Callable, ClassVar, Dict, Iterable, Iterator, List, Optional, Tuple, Union
import warnings

import matplotlib as mpl
import matplotlib.font_manager as fm
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Patch, Rectangle
import matplotlib.pyplot as plt

#: Largest number of blocks a single chart may draw. Blocks cost roughly 36 microseconds each, so
#: this many takes several minutes; the limit is a backstop against values that were meant to be
#: scaled, not a recommendation. Adjust it either way if you need to:
#: ``pywaffle.waffle.MAX_BLOCKS = 1_000_000``.
MAX_BLOCKS = 10_000_000

#: A ListedColormap with at most this many entries is treated as a qualitative palette and used in
#: order. Larger ones are continuous ramps stored as a list of samples, and are sampled across their
#: range instead. Every qualitative colormap matplotlib ships has at most 20 entries (tab20); every
#: continuous one has 256.
QUALITATIVE_COLORMAP_MAX = 20

METHOD_MAPPING = {
    "float": lambda a, b: a / b,
    "nearest": lambda a, b: round(a / b),
    "ceil": lambda a, b: math.ceil(a / b),
    "floor": lambda a, b: a // b,
}


def division(x: int, y: int, method: str = "float") -> Union[int, float]:
    """
    :param x: dividend
    :param y: divisor
    :param method: {'float', 'nearest', 'ceil', 'floor'}
    """
    return METHOD_MAPPING[method.lower()](x, y)


def round_up_to_multiple(x: int, base: int) -> int:
    """
    Round a positive integer up to the nearest multiple of given base number
    For example: 12 -> 15, with base = 5
    """
    return base * math.ceil(x / base)


def array_resize(array: Union[Tuple, List], length: int, array_len: Optional[int] = None) -> Union[Tuple, List]:
    """
    Resize array to given length. If the array is shorter than given length, repeat the array; If the array is longer
    than the length, trim the array.
    :param array: array
    :param length: target length
    :param array_len: if length of original array is known, pass it in here
    :return: resized array
    """
    if not array_len:
        array_len = len(array)
    return array * (length // array_len) + array[: length % array_len]


def chunked(iterable: Iterable, step: int) -> List:
    """Yield successive step-sized chunks from a list."""
    iterable = iter(iterable)
    yield from iter(lambda: list(islice(iterable, step)), [])


def flip_lines(matrix: Iterable[Tuple[int, int]], base: int) -> Tuple[int, int]:
    """Given a matrix in a linear array, flip the element order of every odd row."""
    for line_number, line in enumerate(chunked(matrix, base)):
        yield from line if line_number % 2 == 0 else line[::-1]


class Waffle(Figure):
    """

    A custom Figure class to make waffle charts.

    :param values: Numerical value of each category.

        | If it is a dict, the keys are used as labels.
        | If it is a pandas Series, the index is used as labels.
    :type values: list|dict|pandas.Series

    :param rows: The number of lines of the waffle chart.
    :type rows: int

    :param columns: The number of columns of the waffle chart.

        | At least one of rows and columns is required.
        | If either rows or columns is passed, the other is calculated automatically from the
          sum of values.
        | If both of rows and columns are passed, the block number is fixed and block numbers are
          calculated from scaled values.
    :type columns: int

    :param colors: A list of colors for each category. Its length should be the same as values.

        | Default values are from Set2 colormap.
    :type colors: list[str]|tuple[str], optional

    :param labels: The name of each category.

        | If the values is a dict, this parameter would be replaced by the keys of values.
    :type labels: list[str]|tuple[str], optional

    :param legend: Parameters of matplotlib.pyplot.legend in a dict.

        | E.g. {'loc': '', 'bbox_to_anchor': (,), ...}
        | See full parameter list in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    :type legend: dict, optional

    :param interval_ratio_x: Ratio of horizontal distance between blocks to block's width. [Default 0.2]
    :type interval_ratio_x: float, optional

    :param interval_ratio_y: Ratio of vertical distance between blocks to block's height. [Default 0.2]
    :type interval_ratio_y: float, optional

    :param block_aspect_ratio: The ratio of block's width to height. [Default 1]
    :type block_aspect_ratio: float, optional

    :param cmap_name: Name of colormaps for default color, if colors is not assigned.

        | A qualitative colormap, such as the default 'Set2', is used in order and repeated if there
          are more categories than colors. Any other colormap is sampled evenly across its range, so
          that the categories are visibly distinct.
        | See full list in https://matplotlib.org/stable/users/explain/colors/colormaps.html
        | [Default 'Set2']
    :type cmap_name: str, optional

    :param title: Parameters of matplotlib.axes.Axes.set_title in a dict.

        | E.g. {'label': '', 'fontdict': {}, 'loc': ''}
        | See full parameter list in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.title.html
    :type title: dict, optional

    :param characters: A character in string or a list of characters for each category. [Default None]
    :type icons: str|list[str]|tuple[str], optional

    :param font_size: Font size of Font Awesome icons.

        | The default size is not fixed and depends on the block size.
        | Either a relative value of 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large'
          or 'xx-large', or an absolute font size.
    :type icons: int|str, optional

    :param font_file: Path to custom font file.
    :type icons: str, optional

    :param icons: Icon name of Font Awesome.

        | If it is a string, all categories use the same icon;
        | If it's a list or tuple of icons, the length should be the same as values.
        | See the full list of Font Awesome on https://fontawesome.com/icons?d=gallery&m=free
        | [Default None]
    :type icons: str|list[str]|tuple[str], optional

    :param icon_style: The style of icons to be used.

        | Font Awesome Icons find an icon by style and icon name.
        The style could be 'brands', 'regular' and 'solid'.
        Visit https://fontawesome.com/cheatsheet for detail.

        | If it is a string, it would search icons within given style.
        If it is a list or a tuple, the length should be
        the same as values and it means the style for each icon.

        | [Default 'solid']
    :type icon_style: str|list[str]|tuple[str], optional

    :param icon_size: Font size of Font Awesome icons.

        | Deprecated! Use font_size instead.
        | The default size is not fixed and depends on the block size.
        | Either a relative value of 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large'
          or 'xx-large', or an absolute font size.
    :type icon_size: int|str, optional

    :param icon_legend: Whether to use icon but not color bar in legend. [Default False]
    :type icon_legend: bool, optional

    :param plot_anchor: The alignment method of subplots. ``{'C', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW', 'W'}``

        | See details in https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_anchor.html
        | [Default 'W']
    :type plot_anchor: str, optional

    :param plots: Position and parameters of Waffle class for subplots in a dict,
        with format like {pos: {subplot_args: values, }, }.

        | Pos could be a tuple of three integers, where the first is the number of rows, the
          second the number of columns, and the third the index of the subplot.
        | Pos could also be a 3-digit number, as an int or a string. For example, 235 or '235'
          means the 5th plot on a grid with 2 rows and 3 columns. All three digits must be less
          than 10 for this form to work.
        | The parameters of subplots are the same as Waffle class parameters, excluding plots itself.
        | If any parameter of subplots is not assigned, it use the same parameter in Waffle class as default value.
    :type plots: dict, optional

    :param vertical: Whether to draw the plot vertically or horizontally. [Default False]
    :type vertical: bool, optional

    :param starting_location: Change the starting location plotting the blocks. ``{'NW', 'SW', 'NE', 'SE'}``

        | 'NW' starts from the upper-left, 'SW' from the lower-left, 'NE' from the upper-right
          and 'SE' from the lower-right.
        | [Default 'SW']
    :type starting_location: str, optional

    :param rounding_rule: The rounding rule applied when adjusting values to fit the chart size.
        ``{'nearest', 'floor', 'ceil', 'float'}``

        | When it's 'nearest', it is "round to nearest, ties to even" rounding mode;
        | When it's 'floor', it rounds to less of the two endpoints of the interval;
        | When it's 'ceil', it rounds to greater of the two endpoints of the interval;
        | When it's 'float', values are not rounded at all. Blocks are partially filled where a
          category ends part way through one, and a block containing a boundary between two
          categories is split between their colors. The number of blocks then depends only on the
          total of the values, so charts of equal total are the same size.
        | 'float' draws partially filled rectangles and cannot be combined with ``icons`` or
          ``characters``, which cannot be partially filled.
        | [Default 'nearest']
    :type rounding_rule: str, optional

    :param tight: Set whether and how `.tight_layout` is called when drawing.

        | It could be bool or dict with keys "pad", "w_pad", "h_pad", "rect" or None
        | If a bool, sets whether to call `.tight_layout` upon drawing.
        | If ``None``, use the ``figure.autolayout`` param instead.
        | If a dict, pass it as kwargs to `.tight_layout`, overriding the default paddings.
        | [Default True]
    :type tight: bool|dict, optional

    :param background_color: Color filling the space behind the blocks, including the gaps between them.

        | One rectangle is drawn behind the whole grid, so this works for any block shape and any
          interval ratio, and it applies to icons and characters as well as rectangle blocks.
        | [Default None, no background]
    :type background_color: str, optional

    :param block_edge_color: Color of the border drawn around each block.

        | Only applies to rectangle blocks. Icons and characters are text and have no such border.
        | [Default None, the border matches the block color]
    :type block_edge_color: str, optional

    :param block_edge_width: Width of the border drawn around each block, in points.

        | [Default None, matplotlib's patch line width]
    :type block_edge_width: float, optional

    :param show_values: Append each category's value to its legend label, as ``Label (value)``.

        | ``True`` or ``'value'`` shows the value itself;
        | ``'percentage'`` shows the category's share of the total.
        | [Default False]
    :type show_values: bool|str, optional

    :param value_format: Format string for the number added by ``show_values``.

        | For example ``'{:.2f}%'`` or ``'{:,.0f} units'``.
        | Defaults to ``'{:g}'`` for values and ``'{:.1f}%'`` for percentages.
    :type value_format: str, optional

    :param sort_values: Order the categories by value.

        | ``True`` or ``'desc'`` sorts largest first; ``'asc'`` sorts smallest first.
        | Every per-category argument - ``labels``, ``colors``, ``icons``, ``characters`` and
          ``icon_style`` - is reordered along with the values.
        | [Default False]
    :type sort_values: bool|str, optional

    :param block_arranging_style: Set how to arrange blocks. ``{'normal', 'snake', 'new-line'}``

        | If it is 'normal', it draws blocks line by line with same direction.
        | If it is 'snake', it draws blocks with snake pattern.
        | If it is 'new-line', it starts a new line when drawing each category. This only works
          when just one of ``rows`` and ``columns`` is assigned, with ``vertical=False`` when
          ``rows`` is assigned or ``vertical=True`` when ``columns`` is assigned.
        | [Default 'normal']
    :type block_arranging_style: string, optional
    """

    _direction_values: ClassVar[Dict] = {
        "NW": {"column_order": 1, "row_order": -1},
        "SW": {"column_order": 1, "row_order": 1},
        "NE": {"column_order": -1, "row_order": -1},
        "SE": {"column_order": -1, "row_order": 1},
    }

    _default_parameters: ClassVar[Dict] = {
        "values": [],
        "rows": None,
        "columns": None,
        "colors": None,
        "labels": None,
        "legend": {},
        "characters": None,
        "font_file": None,
        "font_size": None,
        "icons": None,
        "icon_size": None,
        "icon_style": "solid",
        "icon_legend": False,
        "interval_ratio_x": 0.2,
        "interval_ratio_y": 0.2,
        "block_aspect_ratio": 1,
        "cmap_name": "Set2",
        "title": None,
        "plot_anchor": "W",
        "vertical": False,
        "starting_location": "SW",
        "rounding_rule": "nearest",
        "show_values": False,
        "value_format": None,
        "sort_values": False,
        "background_color": None,
        "block_edge_color": None,
        "block_edge_width": None,
        "tight": True,
        "block_arranging_style": "normal",
        "plots": None,
    }

    def __init__(self, *args, **kwargs):
        #: All Waffle-specific arguments with default values
        self.fig_args: Dict = self._kwarg_processor(kwargs=kwargs, default_values=self._default_parameters)
        super().__init__(*args, **kwargs)

        #: Standardized arguments of all subplots
        self.plot_args: List = []

        #: The length of values
        self.values_len: Optional[int] = None

        plots = self.fig_args["plots"] or {111: self.fig_args}

        for loc, plot_args in plots.items():
            # Add subplots
            if isinstance(loc, tuple):
                ax = self.add_subplot(*loc, aspect="equal")
            elif isinstance(loc, (int, str)):
                ax = self.add_subplot(loc, aspect="equal")
            else:
                raise TypeError("Subplot position should be tuple, int, or string.")

            self._make_single_waffle(ax=ax, fig_args=self.fig_args, plot_args=plot_args)

        # Adjust the layout
        self._apply_layout_engine(self.fig_args["tight"])

    @staticmethod
    def _fill_steps(cells: List[Tuple[int, int]], default_axis: int) -> List[Tuple[int, int]]:
        """
        The axis and direction the block sequence travels through each cell.

        A partially filled block fills from the side the sequence arrives at, so this is read off
        the cell order itself rather than derived from ``starting_location``. Reading it per cell
        keeps it correct for the snake style, where the direction reverses on every other line, and
        for a chart one block deep, where the sequence runs along the other axis entirely.
        """

        def unit_step(a, b):
            """The axis and direction from cell a to cell b, or None if they are not neighbours."""
            # A step to the neighbouring cell moves along exactly one axis
            delta = (b[0] - a[0], b[1] - a[1])
            if delta[0] and not delta[1]:
                return 0, 1 if delta[0] > 0 else -1
            if delta[1] and not delta[0]:
                return 1, 1 if delta[1] > 0 else -1
            return None

        steps = []
        for i, cell in enumerate(cells):
            forward = unit_step(cell, cells[i + 1]) if i + 1 < len(cells) else None
            backward = unit_step(cells[i - 1], cell) if i > 0 else None

            # At the end of a line the forward step is the wrap to the next line, which is not the
            # direction the sequence was travelling, so prefer a step along the line axis.
            candidates = [step for step in (forward, backward) if step is not None and step[0] == default_axis]
            candidates += [step for step in (forward, backward) if step is not None]
            steps.append(next(iter(candidates), (default_axis, 1)))
        return steps

    def _draw_fractional_blocks(
        self,
        ax: Axes,
        cells: List[Tuple[int, int]],
        spans: List[Tuple[int, float, float]],
        colors: List,
        block_style: Callable[[object], Dict],
        is_vertical: bool,
        x_full: float,
        y_full: float,
        block_x_length: float,
        block_y_length: float,
    ):
        """
        Draw blocks without rounding the values.

        Each grid cell covers one unit of the block number line, so a category boundary can fall
        inside a cell. Such a cell is drawn as two abutting rectangles, and the last cell of the
        chart is drawn partially filled. The number of cells therefore depends only on the total of
        the values, which is what makes the chart size stable when values change.
        """
        # Blocks advance along rows within a column, unless vertical swaps the two
        steps = self._fill_steps(cells, default_axis=0 if is_vertical else 1)

        for cell_index, (col, row) in enumerate(cells):
            axis, direction = steps[cell_index]
            for class_index, start, end in self._cell_segments(spans, cell_index):
                # Measure the offset from the edge the sequence arrives at
                if direction < 0:
                    start, end = 1 - end, 1 - start

                x, y = x_full * col, y_full * row
                width, height = block_x_length, block_y_length
                if axis == 0:
                    x += start * block_x_length
                    width = (end - start) * block_x_length
                else:
                    y += start * block_y_length
                    height = (end - start) * block_y_length

                ax.add_artist(Rectangle(xy=(x, y), width=width, height=height, **block_style(colors[class_index])))

    @staticmethod
    def _coloured_spans(block_per_cat: List, colored_block_per_cat: List) -> List[Tuple[int, float, float]]:
        """
        Lay the categories out on a continuous number line of blocks.

        Returns ``(class_index, start, end)`` per category, measured in blocks from the start of the
        chart. ``block_per_cat`` is the space a category occupies and ``colored_block_per_cat`` the
        part of it that is coloured; the two differ only for the "new-line" style, where a category
        is padded out to a whole line and the padding stays blank.
        """
        spans = []
        position = 0.0
        for class_index, (occupied, coloured) in enumerate(zip(block_per_cat, colored_block_per_cat)):
            if coloured > 0:
                spans.append((class_index, position, position + coloured))
            position += occupied
        return spans

    @staticmethod
    def _cell_segments(spans: List[Tuple[int, float, float]], cell_index: int) -> List[Tuple[int, float, float]]:
        """
        The portions of one grid cell covered by each category.

        A cell spans ``[cell_index, cell_index + 1)`` on the block number line. Returns
        ``(class_index, start, end)`` with start and end as fractions of the cell, so a cell in the
        middle of a category yields one segment of (0, 1) and a cell straddling a boundary yields
        two segments that between them cover it.
        """
        segments = []
        for class_index, span_start, span_end in spans:
            start = max(span_start, cell_index)
            end = min(span_end, cell_index + 1)
            if end - start > 1e-9:
                segments.append((class_index, start - cell_index, end - cell_index))
        return segments

    @staticmethod
    def _colors_from_cmap(cmap_name: str, length: int) -> List:
        """
        Pick one color per category from a named colormap.

        A qualitative colormap is a designed palette of distinct colors, so it is used in order and
        repeated or trimmed to the number of categories. Anything else is a continuous ramp, and the
        categories are spread evenly across its range.

        The distinction is not the colormap class. matplotlib stores viridis, plasma, magma, cividis
        and turbo as ListedColormaps too, with 256 entries, so taking the first few of those gives
        colors that differ by a fraction of a percent and look identical in a chart. Every
        qualitative colormap matplotlib ships has at most 20 entries and every continuous one has
        256, so the size is what separates them.
        """
        cmap = plt.get_cmap(cmap_name)
        palette = getattr(cmap, "colors", None)

        if palette is not None and cmap.N <= QUALITATIVE_COLORMAP_MAX:
            return array_resize(array=list(palette), length=length, array_len=cmap.N)

        if length == 1:
            return [cmap(0.5)]
        return [cmap(i / (length - 1)) for i in range(length)]

    @staticmethod
    def _block_font_size(ax: Axes, block_x_length: float) -> float:
        """
        Default font size, in points, for an icon or character that should fill one block.

        transData returns display pixels, while font sizes are in points, so the conversion depends
        on the figure's DPI. Assuming a fixed DPI makes icons scale wrongly on any other figure -
        at 200 DPI they come out about twice the intended size.
        """
        (_, y0), (_, y1) = ax.transData.transform([(0, 0), (0, block_x_length)])
        return (y1 - y0) * 72 / ax.figure.dpi

    def _apply_layout_engine(self, tight: Union[bool, Dict, None]):
        """
        Set the layout engine from the ``tight`` argument.

        Figure.set_tight_layout has been deprecated since matplotlib 3.6 in favour of set_layout_engine.
        """
        if tight is None:
            tight = mpl.rcParams["figure.autolayout"]

        if isinstance(tight, dict):
            self.set_layout_engine("tight")
            self.get_layout_engine().set(**tight)
        else:
            self.set_layout_engine("tight" if tight else "none")

    @staticmethod
    def _kwarg_processor(kwargs: Dict, default_values: Dict) -> Dict:
        """
        Given kwargs and default_values in dict, iterate through kwargs and pop all keys in default_values with paired
        default values.
        This is necessary for removing Waffle specific arguments, so the remaining could be passed to parent class
        Figure.
        """
        result = {}
        for arg, val in default_values.items():
            # passing a copy to avoid mutable legend and labels being updated in default_values
            result[arg] = copy.deepcopy(kwargs.pop(arg, val))
        return result

    @staticmethod
    def _block_arranger(
        rows: int,
        columns: int,
        row_order: int,
        column_order: int,
        is_vertical: bool,
        is_snake: bool,
    ) -> Iterator[Tuple[int, int]]:
        """Walk every cell of the grid, from the given starting corner and in the given order."""
        if is_vertical:
            x, x_order, y, y_order = rows, row_order, columns, column_order
            vertical_order = -1
        else:
            x, x_order, y, y_order = columns, column_order, rows, row_order
            vertical_order = 1

        block_matrix = product(range(x)[::x_order], range(y)[::y_order])
        line_base = columns if is_vertical else rows

        if is_snake:
            block_matrix = flip_lines(block_matrix, base=line_base)

        return (c[::vertical_order] for c in block_matrix)

    @staticmethod
    def _block_style(color, edge_color, edge_width) -> Dict:
        """
        Styling for one block.

        Without an edge color, ``color`` is passed through as before, which sets the face and the
        edge to the same value; changing that would shrink every existing chart's blocks by the
        width of the stroke.
        """
        if edge_color is None and edge_width is None:
            return {"color": color}

        style = {"facecolor": color, "edgecolor": edge_color if edge_color is not None else color}
        if edge_width is not None:
            style["linewidth"] = edge_width
        return style

    @staticmethod
    def _sort_categories(par: Dict):
        """
        Reorder the categories by value, carrying every per-category argument along with them.

        Anything given one-per-category - labels, colors, icons, characters, icon_style - has to
        move with its value, or the chart silently mislabels itself. Arguments given as a single
        value apply to every category and need no reordering.
        """
        descending = par["sort_values"] in (True, "desc")
        order = sorted(range(len(par["values"])), key=lambda i: par["values"][i], reverse=descending)

        par["values"] = [par["values"][i] for i in order]
        for name in ("labels", "colors", "icons", "characters", "icon_style"):
            value = par[name]
            if isinstance(value, (list, tuple)) and len(value) == len(order):
                reordered = [value[i] for i in order]
                par[name] = tuple(reordered) if isinstance(value, tuple) else reordered

    @staticmethod
    def _format_values(labels: Iterable, values: List, show_values, value_format: Optional[str]) -> List[str]:
        """
        Append each category's value to its label, as "Label (value)".

        Writing this by hand is what the documentation has always told people to do:
        ``labels=[f"{k} ({v}%)" for k, v in data.items()]``.
        """
        as_percentage = isinstance(show_values, str) and show_values.lower().strip() == "percentage"
        if as_percentage:
            total = sum(values)
            if total == 0:
                raise ValueError('show_values="percentage" needs the values to sum to more than zero.')
            amounts = [v / total * 100 for v in values]
        else:
            amounts = list(values)

        template = value_format or ("{:.1f}%" if as_percentage else "{:g}")
        return [f"{label} ({template.format(amount)})" for label, amount in zip(labels, amounts)]

    @staticmethod
    def _validate_positive_int(par: Dict, name: str):
        """Check that a grid dimension is a positive whole number, if it was given at all.

        Without this, rows=-5 produces columns=-6 and an empty chart with no error, and rows=2.5 or
        rows="5" surface as a TypeError from arithmetic several frames down.
        """
        value = par[name]
        if value is None:
            return

        if isinstance(value, float) and value.is_integer():
            value = int(value)

        try:
            value = operator.index(value)
        except TypeError:
            raise ValueError(f"Argument {name} should be a positive integer, got {value!r}.") from None

        if value <= 0:
            raise ValueError(f"Argument {name} should be a positive integer, got {value!r}.")

        par[name] = value

    @staticmethod
    def _validate_choice(par: Dict, name: str, choices: Tuple[str, ...], case: str):
        """Normalize the case of a string argument and check it against the allowed values."""
        value = par[name]
        if not isinstance(value, str):
            # ValueError rather than TypeError, deliberately: every argument check in this class
            # raises ValueError, so that one `except ValueError` around chart construction catches
            # all of them. Splitting the type case out would defeat that.
            raise ValueError(f"Argument {name} should be a string, one of {', '.join(choices)}.")

        value = value.strip()
        value = value.lower() if case == "lower" else value.upper()
        if value not in choices:
            raise ValueError(f"Argument {name} should be one of {', '.join(choices)}.")

        par[name] = value

    def _parameter_validation(self, par: Dict):
        """Check and normalize every argument, before anything downstream depends on it.

        Validation lives in one place so that a bad argument is reported against its own name rather
        than surfacing as an error from arithmetic or matplotlib several frames later, and so that
        every failure is a ValueError. The steps run in order: the enums first because later checks
        read them, then values, because almost everything else is sized against them.
        """
        self._validate_enums(par)
        self._validate_geometry(par)
        self._validate_values(par)
        self._validate_labels_and_colors(par)

        if par["sort_values"]:
            # Before anything downstream depends on the order
            self._sort_categories(par)

        self._validate_value_numbers(par)
        self._validate_rendering_options(par)
        self._validate_icon_style(par)

    @staticmethod
    def _validate_enums(par: Dict):
        """Normalize and check the arguments that accept a fixed set of strings."""
        Waffle._validate_choice(par, "rounding_rule", ("nearest", "ceil", "floor", "float"), case="lower")
        Waffle._validate_choice(par, "block_arranging_style", ("normal", "snake", "new-line"), case="lower")
        Waffle._validate_choice(par, "starting_location", ("NW", "SW", "NE", "SE"), case="upper")
        # matplotlib's set_anchor does not reject an unknown string, so an unusable anchor is
        # silently stored on the axes and the plot is simply misplaced
        Waffle._validate_choice(par, "plot_anchor", ("C", "SW", "S", "SE", "E", "NE", "N", "NW", "W"), case="upper")

    @staticmethod
    def _validate_geometry(par: Dict):
        """Check the grid dimensions and the block shape arguments."""
        Waffle._validate_positive_int(par, "rows")
        Waffle._validate_positive_int(par, "columns")

        if not isinstance(par["block_aspect_ratio"], numbers.Real) or par["block_aspect_ratio"] <= 0:
            raise ValueError(
                f"Argument block_aspect_ratio should be a positive number, got {par['block_aspect_ratio']!r}."
            )

        for name in ("interval_ratio_x", "interval_ratio_y"):
            if not isinstance(par[name], numbers.Real) or par[name] < 0:
                raise ValueError(f"Argument {name} should be zero or a positive number, got {par[name]!r}.")

    def _validate_values(self, par: Dict):
        """Check values is usable, and unpack a dict or Series into values plus labels."""
        if isinstance(par["values"], str) or not hasattr(par["values"], "__len__"):
            raise ValueError(
                f"Argument values should be a list, tuple, dict or pandas Series, "
                f"got {type(par['values']).__name__}."
            )
        if len(par["values"]) == 0:
            raise ValueError("Argument values is required.")
        self.values_len = len(par["values"])

        if isinstance(par["values"], dict):
            if not par["labels"]:
                par["labels"] = list(par["values"].keys())
            par["values"] = list(par["values"].values())
        elif hasattr(par["values"], "index") and hasattr(par["values"], "tolist"):
            # A pandas Series carries its labels in the index, just as a dict does in its keys
            if not par["labels"]:
                par["labels"] = [str(label) for label in par["values"].index]
            par["values"] = par["values"].tolist()

    def _validate_labels_and_colors(self, par: Dict):
        """Check the per-category arguments are as long as values."""
        if par["colors"] and len(par["colors"]) != self.values_len:
            raise ValueError("Length of colors doesn't match the values.")

        if par["labels"] and len(par["labels"]) != self.values_len:
            raise ValueError("Length of labels doesn't match the values.")

    @staticmethod
    def _validate_value_numbers(par: Dict):
        """Check the values themselves, once they are a plain sequence of numbers."""
        for value in par["values"]:
            if isinstance(value, bool) or not isinstance(value, numbers.Real):
                raise ValueError(f"Argument values should contain only numbers, got {value!r}.")

        if any(v < 0 for v in par["values"]):
            raise ValueError("Argument values should not contain negative numbers.")

        if par["rows"] and par["columns"] and sum(par["values"]) == 0:
            raise ValueError(
                "Argument values should not sum to zero when both rows and columns are given, "
                "as there is no way to scale the values to the chart size."
            )

    @staticmethod
    def _validate_rendering_options(par: Dict):
        """Check the arguments that control what is drawn, and the combinations that cannot work."""
        if par["show_values"] not in (False, True, None) and not (
            isinstance(par["show_values"], str) and par["show_values"].lower().strip() in ("value", "percentage")
        ):
            raise ValueError('Argument show_values should be True, False, "value" or "percentage".')

        # rounding_rule="float" draws partial blocks, which only works for rectangles.
        # A Text artist cannot be partially filled.
        if par["rounding_rule"] == "float" and (par["icons"] or par["characters"]):
            raise ValueError(
                'Argument rounding_rule="float" draws partially filled blocks and cannot be '
                "combined with icons or characters. Use nearest, ceil or floor instead."
            )

    def _validate_icon_style(self, par: Dict):
        """Normalize icon_style to one entry per category, and check every entry is a real style."""
        if not par["icons"]:
            return

        from pywaffle.fontawesome_handler import FA_STYLES

        if isinstance(par["icon_style"], str):
            par["icon_style"] = [par["icon_style"].lower().strip()] * self.values_len
        else:
            par["icon_style"] = [str(i).lower().strip() for i in par["icon_style"]]
            if len(par["icon_style"]) != self.values_len:
                raise ValueError("Length of icon_style doesn't match the values.")

        invalid_styles = sorted(set(par["icon_style"]) - set(FA_STYLES))
        if invalid_styles:
            raise ValueError(
                f"Argument icon_style should be one of {', '.join(FA_STYLES)}. Got {', '.join(invalid_styles)}."
            )

    @classmethod
    def make_waffle(cls, ax: Axes, **kwargs):
        """
        Plot waffle chart on given axis.
        Run it with codes like:
        ``Waffle.make_waffle(ax=ax, rows=5, values=[48, 46, 6])``

        Note that calling this method does not update attributes,
        including ``fig_args``, ``plot_args``, and ``values_len``

        :param ax: An instance of Matplotlib Axes
        :type ax: matplotlib.axes.Axes

        :param **kwargs: Waffle properties

        """
        if kwargs.get("plots"):
            raise ValueError(
                "Argument plots is not supported by make_waffle, which draws into the single axis "
                "given by ax. Use plt.figure(FigureClass=Waffle, plots=...) for subplots."
            )

        w = cls.__new__(cls)

        w._make_single_waffle(
            ax=ax,
            plot_args=cls._kwarg_processor(kwargs=kwargs, default_values=cls._default_parameters),
        )

    def _make_single_waffle(self, ax: Axes, plot_args: Dict, fig_args: Optional[Dict] = None):
        """
        Plot single waffle chart.
        It's for internal use only and do not call this function for plotting directly.

        :param ax: An instance of Matplotlib Axes
        :type ax: matplotlib.axes.Axes

        :param plot_args: Subplot arguments under "plots"
        :type plot_args: dict

        :param fig_args: Figure arguments passed to make_waffle or figure directly
        :type fig_args: dict
        """
        # _pa is the arguments for this single plot
        # Arguments from "plots" have higher priority than figure arguments
        _pa = {**(fig_args or {}), **plot_args}

        self._parameter_validation(par=_pa)

        block_per_cat, colored_block_per_cat = self._resolve_grid(_pa)
        block_x_length, block_y_length = self._setup_axes(ax, _pa)

        if not _pa["colors"]:
            _pa["colors"] = self._colors_from_cmap(_pa["cmap_name"], self.values_len)

        font_properties = self._resolve_glyphs(_pa, ax, block_x_length)

        self._draw_blocks(
            ax=ax,
            par=_pa,
            block_per_cat=block_per_cat,
            colored_block_per_cat=colored_block_per_cat,
            block_x_length=block_x_length,
            block_y_length=block_y_length,
            font_properties=font_properties,
        )

        if _pa["title"] is not None:
            ax.set_title(**_pa["title"])

        self._draw_legend(ax, _pa)

        # Remove borders, ticks, etc.
        ax.axis("off")

        if hasattr(self, "plot_args"):
            self.plot_args.append(_pa)

    @staticmethod
    def _resolve_grid(par: Dict) -> Tuple[List, List]:
        """Work out the grid size and how many blocks each category occupies.

        Returns the blocks a category takes up and the blocks it actually colors. The two differ
        only for the "new-line" style, where a category is padded out to a whole line and the
        padding is left blank. Fills in whichever of rows and columns was not given.
        """
        if not par["rows"] and not par["columns"]:
            raise ValueError("At least one of rows and columns is required.")

        def as_blocks(values):
            """Round each value to a whole number of blocks."""
            return [division(v, 1, method=par["rounding_rule"]) for v in values]

        # When both are given the values are scaled to fill the grid exactly
        if par["rows"] is not None and par["columns"] is not None:
            total = sum(par["values"])
            block_per_cat = colored_block_per_cat = [
                division(v * par["columns"] * par["rows"], total, method=par["rounding_rule"]) for v in par["values"]
            ]
        else:
            # Otherwise the values are block counts, and the missing dimension follows from them
            given, missing = ("columns", "rows") if par["rows"] is None else ("rows", "columns")
            pads_to_whole_lines = par["block_arranging_style"] == "new-line" and (
                par["vertical"] if given == "columns" else not par["vertical"]
            )

            if pads_to_whole_lines:
                block_per_cat = [round_up_to_multiple(v, base=par[given]) for v in par["values"]]
                colored_block_per_cat = as_blocks(par["values"])
            else:
                block_per_cat = colored_block_per_cat = as_blocks(par["values"])

            par[missing] = division(sum(block_per_cat), par[given], method="ceil")

        # A chart is drawn one artist per block, so an unscaled value quietly turns into minutes of
        # drawing rather than an error. Fail fast and say what to do about it.
        total_blocks = par["rows"] * par["columns"]
        if total_blocks > MAX_BLOCKS:
            raise ValueError(
                f"This chart would need {total_blocks:,} blocks, over the limit of {MAX_BLOCKS:,}. "
                f"Pass both rows and columns to scale the values into a fixed grid, or reduce the "
                f"values. Raise pywaffle.waffle.MAX_BLOCKS if you really need a chart this large."
            )

        return block_per_cat, colored_block_per_cat

    @staticmethod
    def _setup_axes(ax: Axes, par: Dict) -> Tuple[float, float]:
        """Set the anchor and axis limits, draw the background, and return the block dimensions."""
        ax.set_anchor(par["plot_anchor"])

        figure_height = 1
        block_y_length = figure_height / (par["rows"] + par["rows"] * par["interval_ratio_y"] - par["interval_ratio_y"])
        block_x_length = par["block_aspect_ratio"] * block_y_length

        chart_width = (
            par["columns"] + par["columns"] * par["interval_ratio_x"] - par["interval_ratio_x"]
        ) * block_x_length
        ax.axis(xmin=0, xmax=chart_width, ymin=0, ymax=figure_height)

        # Fill the gaps between blocks. One rectangle behind the whole grid is enough, and unlike
        # per-block edges it works for any block shape and any interval ratio.
        if par["background_color"] is not None:
            ax.add_artist(
                Rectangle(
                    xy=(0, 0),
                    width=chart_width,
                    height=figure_height,
                    facecolor=par["background_color"],
                    edgecolor="none",
                    zorder=0,
                )
            )

        return block_x_length, block_y_length

    def _resolve_glyphs(self, par: Dict, ax: Axes, block_x_length: float):
        """Resolve icon names to characters and build the font for them.

        Returns the FontProperties the blocks are drawn with, or None when they are rectangles.
        """
        if par["icons"]:
            from pywaffle.fontawesome_handler import icons

            if par["icon_size"]:
                warnings.warn("Parameter icon_size is deprecated. Use font_size instead.", DeprecationWarning)
                par["font_size"] = par["icon_size"]

            # icon_style has already been normalized to a list by _parameter_validation

            # If icons is a string, convert it into a list of same icon. The length is the value's length
            # '\uf26e' -> ['\uf26e', '\uf26e', '\uf26e', ]
            if isinstance(par["icons"], str):
                par["icons"] = [par["icons"]] * self.values_len

            if len(par["icons"]) != self.values_len:
                raise ValueError("Length of icons doesn't match the values.")

            # Replace icon name with Unicode symbols in parameter icons
            par["icons"] = [
                icons[icon_style][icon_name] for icon_name, icon_style in zip(par["icons"], par["icon_style"])
            ]

            return fm.FontProperties(size=par["font_size"] or self._block_font_size(ax, block_x_length))

        if par["characters"]:
            # If characters is a string, convert it into a list of same characters. It's length is the value's length
            if isinstance(par["characters"], str):
                par["characters"] = [par["characters"]] * self.values_len

            if len(par["characters"]) != self.values_len:
                raise ValueError("Length of characters doesn't match the values.")

            return fm.FontProperties(
                size=par["font_size"] or self._block_font_size(ax, block_x_length),
                fname=par["font_file"],
            )

        return None

    def _draw_blocks(
        self,
        ax: Axes,
        par: Dict,
        block_per_cat: List,
        colored_block_per_cat: List,
        block_x_length: float,
        block_y_length: float,
        font_properties,
    ):
        """Walk the grid and draw every block, as a rectangle, an icon or a character."""
        x_full = (1 + par["interval_ratio_x"]) * block_x_length
        y_full = (1 + par["interval_ratio_y"]) * block_y_length

        def block_style(color):
            """Styling keywords for one block of the given colour."""
            return self._block_style(color, par["block_edge_color"], par["block_edge_width"])

        cells = list(
            self._block_arranger(
                rows=par["rows"],
                columns=par["columns"],
                row_order=self._direction_values[par["starting_location"]]["row_order"],
                column_order=self._direction_values[par["starting_location"]]["column_order"],
                is_vertical=par["vertical"],
                is_snake=par["block_arranging_style"] == "snake",
            )
        )

        if par["rounding_rule"] == "float":
            self._draw_fractional_blocks(
                ax=ax,
                cells=cells,
                spans=self._coloured_spans(block_per_cat, colored_block_per_cat),
                colors=par["colors"],
                block_style=block_style,
                is_vertical=par["vertical"],
                x_full=x_full,
                y_full=y_full,
                block_x_length=block_x_length,
                block_y_length=block_y_length,
            )
            return

        draw_block = self._block_drawer(ax, par, block_x_length, block_y_length, font_properties, block_style)

        class_index = 0
        block_index = 0
        this_cat_block_count = 0

        for col, row in cells:
            # Value could be 0. If so, skip it
            while class_index < self.values_len and block_per_cat[class_index] == 0:
                class_index += 1
                this_cat_block_count = 0

            if class_index > self.values_len - 1:
                break

            if this_cat_block_count > colored_block_per_cat[class_index] - 1:
                color = (0, 0, 0, 0)  # transparent
            else:
                color = par["colors"][class_index]

            draw_block(x_full * col, y_full * row, color, class_index)

            # Counted explicitly rather than with enumerate(): this reads as "blocks drawn so
            # far, including this one", which is what the comparison below needs. enumerate would
            # give one less and require a +1 at the point of use.
            block_index += 1
            this_cat_block_count += 1
            if block_index >= sum(block_per_cat[: class_index + 1]):
                class_index += 1
                if class_index > self.values_len - 1:
                    break
                this_cat_block_count = 0

    @staticmethod
    def _block_drawer(ax: Axes, par: Dict, block_x_length: float, block_y_length: float, font_properties, block_style):
        """Return the function that draws one block.

        Which of the three kinds of block a chart uses is fixed for the whole chart, so it is
        decided once here rather than re-tested on every block.
        """
        if par["icons"]:
            from pywaffle.fontawesome_handler import fontawesome_files

            def draw(x, y, color, class_index):
                """Draw one block as a Font Awesome icon."""
                font_properties.set_file(fontawesome_files[par["icon_style"][class_index]])
                ax.text(x=x, y=y, s=par["icons"][class_index], color=color, fontproperties=font_properties)

        elif par["characters"]:

            def draw(x, y, color, class_index):
                """Draw one block as a character."""
                ax.text(x=x, y=y, s=par["characters"][class_index], color=color, fontproperties=font_properties)

        else:

            def draw(x, y, color, class_index):
                """Draw one block as a rectangle."""
                ax.add_artist(Rectangle(xy=(x, y), width=block_x_length, height=block_y_length, **block_style(color)))

        return draw

    def _draw_legend(self, ax: Axes, par: Dict):
        """Build and draw the legend.

        The arguments are built in a new dict rather than mutating par["legend"], which subplots
        share by reference with the figure-level arguments.
        """
        if not (par["labels"] or "labels" in par["legend"]):
            return

        legend_args = {**par["legend"]}
        labels = par["labels"] or legend_args.get("labels")

        if par["show_values"]:
            labels = self._format_values(
                labels=labels,
                values=par["values"],
                show_values=par["show_values"],
                value_format=par["value_format"],
            )

        if par["icons"] and par["icon_legend"] is True:
            from pywaffle.fontawesome_handler import (
                legend_handler_style_mapping,
                legend_style_class_mapping,
            )

            legend_args["handles"] = [
                legend_style_class_mapping[style](color=color, text=icon)
                for color, icon, style in zip(par["colors"], par["icons"], par["icon_style"])
            ]
            legend_args["handler_map"] = legend_handler_style_mapping
        elif not legend_args.get("handles"):
            legend_args["handles"] = [Patch(color=c, label=str(l)) for c, l in zip(par["colors"], labels)]

        # labels is an alias of legend['labels']
        if ("labels" not in legend_args and par["labels"]) or par["show_values"]:
            legend_args["labels"] = labels

        par["legend"] = legend_args

        if "handles" in legend_args and "labels" in legend_args:
            ax.legend(**legend_args)
