#!/usr/bin/python
# -*-coding: utf-8 -*-

from matplotlib.pyplot import cm
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Patch
import matplotlib.font_manager as fm
from matplotlib.text import Text
from matplotlib.legend_handler import HandlerBase
import copy
import os
import font
from itertools import product
import warnings
from typing import List, Tuple, Union


def division(x: int, y: int, method: str = 'float') -> Union[int, float]:
    """
    :param x: dividend
    :param y: divisor
    :param method: {'float', 'nearest', 'ceil', 'floor'}
    """
    method_mapping = {
        'float': lambda a, b: a / b,
        'nearest': lambda a, b: round(a / b),
        'ceil': lambda a, b: int(a // b + bool(a % b)),
        'floor': lambda a, b: a // b,
    }

    return method_mapping[method.lower()](x, y)


def array_resize(array: Union[Tuple, List], length: int, array_len: int = None):
    """
    Resize array to given length. If the array is shorter than given length, repeat the array; If the array is longer
    than the length, trim the array.
    :param array: array
    :param length: target length
    :param array_len: if length of original array is known, pass it in here
    :return: axtended array
    """
    if not array_len:
        array_len = len(array)
    return array * (length // array_len) + array[:length % array_len]


_FONT_PATH = font.__path__[0]
FONTAWESOME_FILES = {
    'brands': os.path.join(_FONT_PATH, 'Font Awesome 5 Brands-Regular-400.otf'),
    'solid': os.path.join(_FONT_PATH, 'Font Awesome 5 Free-Solid-900.otf'),
    'regular': os.path.join(_FONT_PATH, 'Font Awesome 5 Free-Regular-400.otf'),
}


class TextLegendBase(object):
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


LEGENDSTYLE = {'solid': SolidTextLegend, 'regular': RegularTextLegend, 'brands': BrandsTextLegend}


class TextLegendHandler(HandlerBase):
    def __init__(self, font_file):
        super().__init__()
        self.font_file = font_file

    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        x = xdescent + width / 2.0
        y = ydescent + height / 2.0
        kwargs = {
            'horizontalalignment': 'center',
            'verticalalignment': 'center',
            'color': orig_handle.color,
            'fontproperties': fm.FontProperties(fname=self.font_file, size=fontsize)
        }
        kwargs.update(orig_handle.kwargs)
        annotation = Text(x, y, orig_handle.text, **kwargs)
        return [annotation]


HANDLER_MAP = {
    SolidTextLegend: TextLegendHandler(FONTAWESOME_FILES['solid']),
    RegularTextLegend: TextLegendHandler(FONTAWESOME_FILES['regular']),
    BrandsTextLegend: TextLegendHandler(FONTAWESOME_FILES['brands'])
}


class Waffle(Figure):
    """

    A custom Figure class to make waffle charts.

    :param values: Numerical value of each category. If it is a dict, the keys would be used as labels.
    :type values: list|dict|pandas.Series

    :param rows: The number of lines of the waffle chart. This is required unless it is specified in argument plots.
    :type rows: int

    :param columns: The number of columns of the waffle chart.
        If it is not None, the total number of blocks would be decided through rows and columns. [Default None]
    :type columns: int

    :param colors: A list of colors for each category. Its length should be the same as values.
        Default values are from Set2 colormap.
    :type colors: list[str]|tuple[str]

    :param labels: The name of each category.
        If the values is a dict, this parameter would be replaced by the keys of values.
    :type labels: list[str]|tuple[str]

    :param legend: Parameters of matplotlib.pyplot.legend in a dict.
        E.g. {'loc': '', 'bbox_to_anchor': (,), ...}
        See full parameter list in https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    :type legend: dict

    :param interval_ratio_x: Ratio of horizontal distance between blocks to block's width. [Default 0.2]
    :type interval_ratio_x: float

    :param interval_ratio_y: Ratio of vertical distance between blocks to block's height. [Default 0.2]
    :type interval_ratio_y: float

    :param block_aspect_ratio: The ratio of block's width to height. [Default 1]
    :type block_aspect_ratio: float

    :param cmap_name: Name of colormaps for default color, if colors is not assigned.
        See full list in https://matplotlib.org/examples/color/colormaps_reference.html [Default 'Set2']
    :type cmap_name: str

    :param title: Parameters of matplotlib.axes.Axes.set_title in a dict.
        E.g. {'label': '', 'fontdict': {}, 'loc': ''}
        See full parameter list in https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_title.html
    :type title: dict

    :param icons: Icon name of Font Awesome. If it is a string, all categories use the same icon;
        If it's a list or tuple of icons, the length should be the same as values.
        See the full list of Font Awesome on https://fontawesome.com/icons?d=gallery&m=free [Default None]
    :type icons: str|list[str]|tuple[str]

    :param icon_set: Deprecated. {'brands', 'regular', 'solid'}
        The style of icons to be used.
        [Default 'solid']
    :type icon_set: str|list[str]|tuple[str]

    :param icon_style: The style of icons to be used.
        Font Awesome Icons find an icon by style and icon name. The style could be 'brands', 'regular' and 'solid'.
        Visit https://fontawesome.com/cheatsheet for detail.
        If it is a string, it would search icons within given style. If it is a list or a tuple, the length should be
        the same as values and it means the style for each icon.
        [Default 'solid']
    :type icon_style: str|list[str]|tuple[str]

    :param icon_size: Fint size of the icons.
    The default size is not fixed and depends on the block size.
    Either an relative value of 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large' or an absolute font size, e.g., 12
    :type icon_size: int

    :param icon_legend: Whether to use icon but not color bar in legend. [Default False]
    :type icon_legend: bool

    :param plot_anchor: {'C', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW', 'W'}
        The alignment method of subplots.
        See details in https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.set_anchor.html
        [Default 'W']
    :type plot_anchor: str

    :param plots: Location and parameters of Waffle class for subplots in a dict,
        with format like {loc: {subplot_args: values, }, }.
        loc is a 3-digit integer. If the three integers are I, J, and K,
        the subplot is the Ith plot on a grid with J rows and K columns.
        The parameters of subplots are the same as Waffle class parameters, excluding plots itself.
        Nested subplots is not supported.
        If any parameter of subplots is not assigned, it use the same parameter in Waffle class as default value.
    :type plots: dict

    :param plot_direction: Deprecated. {'NW', 'SW', 'NE', 'SE'}
        Use starting_location instead.
        Change the starting location plotting the blocks.
        'NW' means plots start at upper left and end at lower right;
        For 'SW', plots start at lower left and end at upper right;
        For 'NE', plots start at upper right and end at lower left;
        For 'SE', plots start at lower right and end at upper left.
        [Default 'SW']
    :type plot_direction: str

    :param vertical: decide whether to draw the plot vertically or horizontally.
        [Default False]
    :type vertical: bool

    :param starting_location: {'NW', 'SW', 'NE', 'SE'}.
        Change the starting location plotting the blocks
        'NW' means plots start at upper left;
        For 'SW', plots start at lower left;
        For 'NE', plots start at upper right;
        For 'SE', plots start at lower right.
        [Default 'SW']
    :type plot_direction: str

    :param rounding_rule: {'nearest', 'floor', 'ceil'}.
        The rounding rule applied when shrinking values to fit the chart size.
        'nearest' means "round to nearest, ties to even" rounding mode;
        'floor' means round to less of the two endpoints of the interval;
        'ceil' means round to greater of the two endpoints of the interval.
        [Default 'nearest']
    :type rounding_rule: str
    """

    _direction_values = {
        'NW': {
            'column_order': 1,
            'row_order': -1,
        },
        'SW': {
            'column_order': 1,
            'row_order': 1,
        },
        'NE': {
            'column_order': -1,
            'row_order': 1,
        },
        'SE': {
            'column_order': -1,
            'row_order': -1,
        },
    }

    def __init__(self, *args, **kwargs):
        self.fig_args = {
            'values': kwargs.pop('values', []),
            'rows': kwargs.pop('rows', None),
            'columns': kwargs.pop('columns', None),
            'colors': kwargs.pop('colors', None),
            'labels': kwargs.pop('labels', None),
            'legend': kwargs.pop('legend', {}),
            'icons': kwargs.pop('icons', None),
            'icon_size': kwargs.pop('icon_size', None),
            'icon_set': kwargs.pop('icon_set', 'solid'),  # Deprecated
            'icon_style': kwargs.pop('icon_style', 'solid'),
            'icon_legend': kwargs.pop('icon_legend', False),
            'interval_ratio_x': kwargs.pop('interval_ratio_x', 0.2),
            'interval_ratio_y': kwargs.pop('interval_ratio_y', 0.2),
            'block_aspect_ratio': kwargs.pop('block_aspect_ratio', 1),
            'cmap_name': kwargs.pop('cmap_name', 'Set2'),
            'title': kwargs.pop('title', None),
            'plot_anchor': kwargs.pop('plot_anchor', 'W'),
            'plot_direction': kwargs.pop('plot_direction', ''),  # Deprecated
            'vertical': kwargs.pop('vertical', False),
            'starting_location': kwargs.pop('starting_location', 'SW'),
            'rounding_rule': kwargs.pop('rounding_rule', 'nearest'),
        }
        self.plots = kwargs.pop('plots', None)

        # If plots is empty, make a single waffle chart
        if self.plots is None:
            self.plots = {111: self.fig_args}

        Figure.__init__(self, *args, **kwargs)

        for loc, setting in self.plots.items():
            self._waffle(loc, **copy.deepcopy(setting))

        # Adjust the layout
        self.set_tight_layout(True)

    def _waffle(self, loc, **kwargs):
        # _pa is the arguments for this single plot
        self._pa = kwargs

        # Append figure args to plot args
        plot_fig_args = copy.deepcopy(self.fig_args)
        for arg, v in plot_fig_args.items():
            if arg not in self._pa:
                self._pa[arg] = v

        # Parameter Validation
        self._pa['rounding_rule'] = self._pa['rounding_rule'].lower()
        if self._pa['rounding_rule'] not in ('nearest', 'ceil', 'floor'):
            raise ValueError("Argument rounding_rule should be one of nearest, ceil or floor.")

        if len(self._pa['values']) == 0 or not self._pa['rows']:
            raise ValueError("Argument values or rows is required.")

        self.values_len = len(self._pa['values'])

        if self._pa['colors'] and len(self._pa['colors']) != self.values_len:
            raise ValueError("Length of colors doesn't match the values.")

        # lebels and values
        if isinstance(self._pa['values'], dict):
            if not self._pa['labels']:
                self._pa['labels'] = self._pa['values'].keys()
            self._pa['values'] = list(self._pa['values'].values())

        if self._pa['labels'] and len(self._pa['labels']) != self.values_len:
            raise ValueError("Length of labels doesn't match the values.")

        self.ax = self.add_subplot(loc, aspect='equal')

        # Alignment of subplots
        self.ax.set_anchor(self._pa['plot_anchor'])

        self.value_sum = sum(self._pa['values'])

        # if column number is not given, use the values as number of blocks
        if self._pa['columns'] is None:
            self._pa['columns'] = division(self.value_sum, self._pa['rows'], method='ceil')
            block_number_per_cat = self._pa['values']
        else:
            block_number_per_cat = [
                division(v * self._pa['columns'] * self._pa['rows'], self.value_sum, method=self._pa['rounding_rule'])
                for v in self._pa['values']
            ]

        # Absolute height of the plot
        figure_height = 1
        block_y_length = figure_height / (
            self._pa['rows'] + self._pa['rows'] * self._pa['interval_ratio_y'] - self._pa['interval_ratio_y']
        )
        block_x_length = self._pa['block_aspect_ratio'] * block_y_length

        # Define the limit of X, Y axis
        self.ax.axis(
            xmin=0,
            xmax=(
                self._pa['columns'] + self._pa['columns'] * self._pa['interval_ratio_x'] - self._pa['interval_ratio_x']
            ) * block_x_length,
            ymin=0,
            ymax=figure_height
        )

        # Build a color sequence if colors is empty
        if not self._pa['colors']:
            default_colors = cm.get_cmap(self._pa['cmap_name']).colors
            default_color_num = cm.get_cmap(self._pa['cmap_name']).N
            self._pa['colors'] = array_resize(array=default_colors, length=self.values_len, array_len=default_color_num)

        # Set icons
        if self._pa['icons']:
            from pywaffle.fontawesome_mapping import icons

            # TODO: deprecating icon_set
            if self._pa['icon_set'] != 'solid' and self._pa['icon_style'] == 'solid':
                self._pa['icon_style'] = self._pa['icon_set']
                warnings.warn(
                    "Parameter icon_set is deprecated and will be removed in future version. Use icon_style instead.",
                    DeprecationWarning
                )

            # If icon_set is a string, convert it into a list of same icon. It's length is the label's length
            # 'solid' -> ['solid', 'solid', 'solid', ]
            if isinstance(self._pa['icon_style'], str):
                self._pa['icon_style'] = [self._pa['icon_style'].lower()] * self.values_len
            elif set(self._pa['icon_style']) - set(icons.keys()):
                raise KeyError('icon_set should be one of {}'.format(', '.join(icons.keys())))

            # If icons is a string, convert it into a list of same icon. It's length is the label's length
            # '\uf26e' -> ['\uf26e', '\uf26e', '\uf26e', ]
            if isinstance(self._pa['icons'], str):
                self._pa['icons'] = [self._pa['icons']] * self.values_len

            if len(self._pa['icons']) != self.values_len:
                raise ValueError("Length of icons doesn't match the values.")

            # Replace icon name with Unicode symbols in parameter icons
            self._pa['icons'] = [
                icons[icon_style][icon_name]
                for icon_name, icon_style in zip(self._pa['icons'], self._pa['icon_style'])
            ]

            # Calculate icon size based on the block size
            tx, ty = self.ax.transData.transform([(0, 0), (0, block_x_length)])
            prop = fm.FontProperties(size=self._pa['icon_size'] or int((ty[1] - tx[1]) / 16 * 12))

        plot_direction = self._pa['plot_direction'].upper()

        if plot_direction:
            warnings.warn(
                "Parameter plot_direction is deprecated and will be removed in future version. Use starting_location instead.",
                DeprecationWarning
            )
            starting_location = self._pa['plot_direction'].upper()
        else:
            # TODO: starting_location will replace plot_direction in 0.3.0
            starting_location = self._pa['starting_location'].upper()

        try:
            column_order = self._direction_values[starting_location]['column_order']
            row_order = self._direction_values[starting_location]['row_order']
        except KeyError:
            raise KeyError("starting_location should be one of 'NW', 'SW', 'NE', 'SE'")

        if self.fig_args['vertical']:
            block_iter = [
                c[::-1]
                for c in product(range(self._pa['rows'])[::row_order],
                                 range(self._pa['columns'])[::column_order])
            ]
        else:
            block_iter = product(range(self._pa['columns'])[::column_order], range(self._pa['rows'])[::row_order])

        # Plot blocks
        class_index = 0
        block_index = 0
        x_full = (1 + self._pa['interval_ratio_x']) * block_x_length
        y_full = (1 + self._pa['interval_ratio_y']) * block_y_length

        for col, row in block_iter:
            if block_number_per_cat[class_index] == 0:
                class_index += 1

                if class_index > self.values_len - 1:
                    break
            elif block_number_per_cat[class_index] < 0:
                raise ValueError("Negative value is not acceptable")

            x = x_full * col
            y = y_full * row

            if self._pa['icons']:
                prop.set_file(FONTAWESOME_FILES[self._pa['icon_style'][class_index]])
                self.ax.text(
                    x=x,
                    y=y,
                    s=self._pa['icons'][class_index],
                    color=self._pa['colors'][class_index],
                    fontproperties=prop
                )
            else:
                self.ax.add_artist(
                    Rectangle(
                        xy=(x, y), width=block_x_length, height=block_y_length, color=self._pa['colors'][class_index]
                    )
                )

            block_index += 1
            if block_index >= sum(block_number_per_cat[:class_index + 1]):
                class_index += 1
                if class_index > self.values_len - 1:
                    break

        # Add title
        if self._pa['title'] is not None:
            self.ax.set_title(**self._pa['title'])

        # Add legend
        if self._pa['labels'] or 'labels' in self._pa['legend']:
            labels = self._pa['labels'] or self._pa['legend'].get('labels')
            if self._pa['icons'] and self._pa['icon_legend'] is True:
                self._pa['legend']['handles'] = [
                    LEGENDSTYLE[style](color=color, text=icon)
                    for color, icon, style in zip(self._pa['colors'], self._pa['icons'], self._pa['icon_style'])
                ]
                self._pa['legend']['handler_map'] = HANDLER_MAP
            # elif not self._pa['legend'].get('handles'):
            elif 'handles' not in self._pa['legend']:
                self._pa['legend']['handles'] = [
                    Patch(color=c, label=str(l)) for c, l in zip(self._pa['colors'], labels)
                ]

            # labels is an alias of legend['labels']
            if 'labels' not in self._pa['legend'] and self._pa['labels']:
                self._pa['legend']['labels'] = self._pa['labels']

            if 'handles' in self._pa['legend'] and 'labels' in self._pa['legend']:
                self.ax.legend(**self._pa['legend'])

        # Remove borders, ticks, etc.
        self.ax.axis('off')

    def remove(self):
        pass
