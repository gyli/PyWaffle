#!/usr/bin/python
# -*-coding: utf-8 -*-

import copy
import math
from itertools import islice, product
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union
import warnings

import matplotlib as mpl
import matplotlib.font_manager as fm
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Patch, Rectangle
import matplotlib.pyplot as plt

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


def array_resize(
    array: Union[Tuple, List], length: int, array_len: int = None
) -> Union[Tuple, List]:
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
    """
    Yield successive step-sized chunks from list
    """
    iterable = iter(iterable)
    yield from iter(lambda: list(islice(iterable, step)), [])


def flip_lines(matrix: Iterable[Tuple[int, int]], base: int) -> Tuple[int, int]:
    """
    Given a matrix in a linear array, flip the element order of every odd row
    """
    for line_number, line in enumerate(chunked(matrix, base)):
        yield from line if line_number % 2 == 0 else line[::-1]


class Waffle(Figure):
    """

    A custom Figure class to make waffle charts.

    :param values: Numerical value of each category. If it is a dict, the keys would be used as labels.
    :type values: list|dict|pandas.Series

    :param rows: The number of lines of the waffle chart.
    :type rows: int

    :param columns: The number of columns of the waffle chart.

        | At least one of rows and columns is required.
        | If either rows or columns is passed, the other parameter would be calculated automatically through the absolute value of values.
        | If both of rows and columns are passed, the block number is fixed and block numbers are calculated from scaled values.
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

        | See full list in https://matplotlib.org/examples/color/colormaps_reference.html
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
        | Either an relative value of 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large' or an absolute font size.
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
        | Either an relative value of 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large' or an absolute value of font size.
    :type icon_size: int|str, optional

    :param icon_legend: Whether to use icon but not color bar in legend. [Default False]
    :type icon_legend: bool, optional

    :param plot_anchor: The alignment method of subplots. ``{'C', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW', 'W'}``

        | See details in https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_anchor.html
        | [Default 'W']
    :type plot_anchor: str, optional

    :param plots: Position and parameters of Waffle class for subplots in a dict,
        with format like {pos: {subplot_args: values, }, }.

        | Pos could be a tuple of three integer, where the first digit is the number of rows, the second the number of columns, and the third the index of the subplot.
        | Pos could also be a 3-digit number in int or string type. For example, it accept 235 or '235' standing for the Ith plot on a grid with J rows and K columns. Note that all integers must be less than 10 for this form to work.
        | The parameters of subplots are the same as Waffle class parameters, excluding plots itself.
        | If any parameter of subplots is not assigned, it use the same parameter in Waffle class as default value.
    :type plots: dict, optional

    :param vertical: Whether to draw the plot vertically or horizontally. [Default False]
    :type vertical: bool, optional

    :param starting_location: Change the starting location plotting the blocks. ``{'NW', 'SW', 'NE', 'SE'}``

        | When it's 'NW', it means plots start from upper-left; 'SW' means plots start from lower-left; 'NE' means plots start from upper-right; 'SE' means plots start from lower-right.
        | [Default 'SW']
    :type starting_location: str, optional

    :param rounding_rule: The rounding rule applied when adjusting values to fit the chart size. ``{'nearest', 'floor', 'ceil'}``

        | When it's 'nearest', it is "round to nearest, ties to even" rounding mode;
        | When it's 'floor', it rounds to less of the two endpoints of the interval;
        | When it's 'ceil', it rounds to greater of the two endpoints of the interval.
        | [Default 'nearest']
    :type rounding_rule: str, optional

    :param tight: Set whether and how `.tight_layout` is called when drawing.

        | It could be bool or dict with keys "pad", "w_pad", "h_pad", "rect" or None
        | If a bool, sets whether to call `.tight_layout` upon drawing.
        | If ``None``, use the ``figure.autolayout`` param instead.
        | If a dict, pass it as kwargs to `.tight_layout`, overriding the default paddings.
        | [Default True]
    :type tight: bool|dict, optional

    :param block_arranging_style: Set how to arrange blocks. ``{'normal', 'snake', 'new-line'}``

        | If it is 'normal', it draws blocks line by line with same direction.
        | If it is 'snake', it draws blocks with snake pattern.
        | If it is 'new-line', it starts with a new line when drawing each category. This only works when only one of ``rows`` and ``columns`` is assigned, and ``vertical=False`` when ``rows`` is assigned or ``vertical=True`` when ``rows`` is assigned.
        | [Default 'normal']
    :type block_arranging_style: string, optional
    """

    _direction_values = {
        "NW": {"column_order": 1, "row_order": -1},
        "SW": {"column_order": 1, "row_order": 1},
        "NE": {"column_order": -1, "row_order": -1},
        "SE": {"column_order": -1, "row_order": 1},
    }

    _default_parameters = {
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
        "tight": True,
        "block_arranging_style": "normal",
        "plots": None,
    }

    def __init__(self, *args, **kwargs):
        #:All Waffle-specific arguments with default values
        self.fig_args: Dict = self._kwarg_processor(
            kwargs=kwargs, default_values=self._default_parameters
        )
        super().__init__(*args, **kwargs)

        #:Standardized arguments of all subplots
        self.plot_args: List = []

        #:The length of values
        self.values_len: Optional[int] = None

        plots = self.fig_args["plots"] or {} or {111: self.fig_args}

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
    def _colors_from_cmap(cmap_name: str, length: int) -> List:
        """
        Pick one color per category from a named colormap.

        A discrete (listed) colormap has a fixed palette, which is repeated or trimmed to the number
        of categories. A continuous colormap has no such palette, so the categories are spread evenly
        across its range instead. Reaching for .colors on a continuous colormap raises AttributeError.
        """
        cmap = plt.get_cmap(cmap_name)
        palette = getattr(cmap, "colors", None)
        if palette is not None:
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
        """
        Given the size of a matrix and starting point, return how to go through every element in the matrix
        """
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
    def _validate_choice(par: Dict, name: str, choices: Tuple[str, ...], case: str):
        """
        Normalize the case of a string argument and check it against the allowed values.
        """
        value = par[name]
        if not isinstance(value, str):
            raise ValueError(
                f"Argument {name} should be a string, one of {', '.join(choices)}."
            )

        value = value.strip()
        value = value.lower() if case == "lower" else value.upper()
        if value not in choices:
            raise ValueError(
                f"Argument {name} should be one of {', '.join(choices)}."
            )

        par[name] = value

    def _parameter_validation(self, par: Dict):
        # - rounding_rule, block_arranging_style, starting_location
        self._validate_choice(
            par, "rounding_rule", ("nearest", "ceil", "floor"), case="lower"
        )
        self._validate_choice(
            par,
            "block_arranging_style",
            ("normal", "snake", "new-line"),
            case="lower",
        )
        self._validate_choice(
            par, "starting_location", ("NW", "SW", "NE", "SE"), case="upper"
        )

        # - values
        if len(par["values"]) == 0:
            raise ValueError("Argument values is required.")
        self.values_len = len(par["values"])

        # - color
        if par["colors"] and len(par["colors"]) != self.values_len:
            raise ValueError("Length of colors doesn't match the values.")

        # - labels and values
        if isinstance(par["values"], dict):
            if not par["labels"]:
                par["labels"] = list(par["values"].keys())
            par["values"] = list(par["values"].values())

        if par["labels"] and len(par["labels"]) != self.values_len:
            raise ValueError("Length of labels doesn't match the values.")

        # - values, after they are guaranteed to be a sequence of numbers
        if any(v < 0 for v in par["values"]):
            raise ValueError("Argument values should not contain negative numbers.")

        if par["rows"] and par["columns"] and sum(par["values"]) == 0:
            raise ValueError(
                "Argument values should not sum to zero when both rows and columns are given, "
                "as there is no way to scale the values to the chart size."
            )

        # - icon_style
        if par["icons"]:
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
                    f"Argument icon_style should be one of {', '.join(FA_STYLES)}. "
                    f"Got {', '.join(invalid_styles)}."
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
        w = cls.__new__(cls)

        w._make_single_waffle(
            ax=ax,
            plot_args=cls._kwarg_processor(
                kwargs=kwargs, default_values=cls._default_parameters
            ),
        )

    def _make_single_waffle(self, ax: Axes, plot_args: Dict, fig_args: Dict = {}):
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
        _pa = {**fig_args, **plot_args}

        self._parameter_validation(par=_pa)

        # Alignment of subplots
        ax.set_anchor(_pa["plot_anchor"])

        # if only one of rows/columns given, use the values as number of blocks
        if not _pa["rows"] and not _pa["columns"]:
            raise ValueError("At least one of rows and columns is required.")
        # if columns is given, rows is not
        elif _pa["rows"] is None:
            if _pa["block_arranging_style"] == "new-line" and _pa["vertical"]:
                block_per_cat = [
                    round_up_to_multiple(i, base=_pa["columns"]) for i in _pa["values"]
                ]
                colored_block_per_cat = [
                    division(v, 1, method=_pa["rounding_rule"]) for v in _pa["values"]
                ]
            else:
                block_per_cat = colored_block_per_cat = [
                    division(v, 1, method=_pa["rounding_rule"]) for v in _pa["values"]
                ]
            _pa["rows"] = division(sum(block_per_cat), _pa["columns"], method="ceil")
        # if rows is given, columns is not
        elif _pa["columns"] is None:
            if _pa["block_arranging_style"] == "new-line" and not _pa["vertical"]:
                block_per_cat = [
                    round_up_to_multiple(i, base=_pa["rows"]) for i in _pa["values"]
                ]
                colored_block_per_cat = [
                    division(v, 1, method=_pa["rounding_rule"]) for v in _pa["values"]
                ]
            else:
                block_per_cat = colored_block_per_cat = [
                    division(v, 1, method=_pa["rounding_rule"]) for v in _pa["values"]
                ]
            _pa["columns"] = division(sum(block_per_cat), _pa["rows"], method="ceil")
        # if both of rows and columns are given
        else:
            block_per_cat = colored_block_per_cat = [
                division(
                    v * _pa["columns"] * _pa["rows"],
                    sum(_pa["values"]),
                    method=_pa["rounding_rule"],
                )
                for v in _pa["values"]
            ]

        # Absolute height of the plot
        figure_height = 1
        block_y_length = figure_height / (
            _pa["rows"]
            + _pa["rows"] * _pa["interval_ratio_y"]
            - _pa["interval_ratio_y"]
        )
        block_x_length = _pa["block_aspect_ratio"] * block_y_length

        # Define the limit of X, Y axis
        ax.axis(
            xmin=0,
            xmax=(
                _pa["columns"]
                + _pa["columns"] * _pa["interval_ratio_x"]
                - _pa["interval_ratio_x"]
            )
            * block_x_length,
            ymin=0,
            ymax=figure_height,
        )

        # Build a color sequence if colors is empty
        if not _pa["colors"]:
            _pa["colors"] = self._colors_from_cmap(_pa["cmap_name"], self.values_len)

        # Set icons
        if _pa["icons"]:
            from pywaffle.fontawesome_handler import fontawesome_files, icons

            if _pa["icon_size"]:
                warnings.warn("Parameter icon_size is deprecated. Use font_size instead.", DeprecationWarning)
                _pa["font_size"] = _pa["icon_size"]

            # icon_style has already been normalized to a list by _parameter_validation

            # If icons is a string, convert it into a list of same icon. The length is the value's length
            # '\uf26e' -> ['\uf26e', '\uf26e', '\uf26e', ]
            if isinstance(_pa["icons"], str):
                _pa["icons"] = [_pa["icons"]] * self.values_len

            if len(_pa["icons"]) != self.values_len:
                raise ValueError("Length of icons doesn't match the values.")

            # Replace icon name with Unicode symbols in parameter icons
            _pa["icons"] = [
                icons[icon_style][icon_name]
                for icon_name, icon_style in zip(_pa["icons"], _pa["icon_style"])
            ]

            prop = fm.FontProperties(
                size=_pa["font_size"] or self._block_font_size(ax, block_x_length)
            )

        elif _pa["characters"]:
            # If characters is a string, convert it into a list of same characters. It's length is the value's length
            if isinstance(_pa["characters"], str):
                _pa["characters"] = [_pa["characters"]] * self.values_len

            if len(_pa["characters"]) != self.values_len:
                raise ValueError("Length of characters doesn't match the values.")

            prop = fm.FontProperties(
                size=_pa["font_size"] or self._block_font_size(ax, block_x_length),
                fname=_pa["font_file"],
            )

        # Plot blocks
        class_index = 0
        block_index = 0
        this_cat_block_count = 0
        x_full = (1 + _pa["interval_ratio_x"]) * block_x_length
        y_full = (1 + _pa["interval_ratio_y"]) * block_y_length
        column_order = self._direction_values[_pa["starting_location"]]["column_order"]
        row_order = self._direction_values[_pa["starting_location"]]["row_order"]

        for col, row in self._block_arranger(
            rows=_pa["rows"],
            columns=_pa["columns"],
            row_order=row_order,
            column_order=column_order,
            is_vertical=_pa["vertical"],
            is_snake=_pa["block_arranging_style"] == "snake",
        ):
            # Value could be 0. If so, skip it
            while class_index < self.values_len and block_per_cat[class_index] == 0:
                class_index += 1
                this_cat_block_count = 0

            if class_index > self.values_len - 1:
                break

            if this_cat_block_count > colored_block_per_cat[class_index] - 1:
                color = (0, 0, 0, 0)  # transparent
            else:
                color = _pa["colors"][class_index]

            x = x_full * col
            y = y_full * row

            if _pa["icons"]:
                prop.set_file(fontawesome_files[_pa["icon_style"][class_index]])
                ax.text(
                    x=x,
                    y=y,
                    s=_pa["icons"][class_index],
                    color=color,
                    fontproperties=prop,
                )
            elif _pa["characters"]:
                ax.text(
                    x=x,
                    y=y,
                    s=_pa["characters"][class_index],
                    color=color,
                    fontproperties=prop,
                )
            else:
                ax.add_artist(
                    Rectangle(
                        xy=(x, y),
                        width=block_x_length,
                        height=block_y_length,
                        color=color,
                    )
                )

            block_index += 1
            this_cat_block_count += 1
            if block_index >= sum(block_per_cat[: class_index + 1]):
                class_index += 1
                if class_index > self.values_len - 1:
                    break
                this_cat_block_count = 0

        # Add title
        if _pa["title"] is not None:
            ax.set_title(**_pa["title"])

        # Add legend
        # The arguments are built in a new dict rather than mutating _pa["legend"], which subplots
        # share by reference with the figure-level arguments
        if _pa["labels"] or "labels" in _pa["legend"]:
            legend_args = {**_pa["legend"]}
            labels = _pa["labels"] or legend_args.get("labels")

            if _pa["icons"] and _pa["icon_legend"] is True:
                from pywaffle.fontawesome_handler import (
                    legend_handler_style_mapping,
                    legend_style_class_mapping,
                )

                legend_args["handles"] = [
                    legend_style_class_mapping[style](color=color, text=icon)
                    for color, icon, style in zip(
                        _pa["colors"], _pa["icons"], _pa["icon_style"]
                    )
                ]
                legend_args["handler_map"] = legend_handler_style_mapping
            elif not legend_args.get("handles"):
                legend_args["handles"] = [
                    Patch(color=c, label=str(l)) for c, l in zip(_pa["colors"], labels)
                ]

            # labels is an alias of legend['labels']
            if "labels" not in legend_args and _pa["labels"]:
                legend_args["labels"] = _pa["labels"]

            _pa["legend"] = legend_args

            if "handles" in legend_args and "labels" in legend_args:
                ax.legend(**legend_args)

        # Remove borders, ticks, etc.
        ax.axis("off")

        if hasattr(self, "plot_args"):
            self.plot_args.append(_pa)
