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


def ceil(a, b):
    """
    Just like math.ceil
    """
    return int(a // b + bool(a % b))


def array_resize(array, length, array_len=None):
    """
    Resize array to given length
    :param array: array
    :param length: target length
    :param array_len: if length of original array is known, pass it in here
    :return: axtended array
    """
    if not array_len:
        array_len = len(array)
    return array * (length // array_len) + array[:length % array_len]


def unique_pairs(w, h):
    for i in range(w):
        for j in range(h):
            yield i, j


FONTAWESOME_FILE = os.path.join(font.__path__[0], 'FontAwesome.otf')


class TextLegend(object):
    def __init__(self, text, color, **kwargs):
        self.text = text
        self.color = color
        self.kwargs = kwargs


class TextLegendHandler(HandlerBase):
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        x = xdescent + width / 2.0
        y = ydescent + height / 2.0
        kwargs = {
            'horizontalalignment': 'center',
            'verticalalignment': 'center',
            'color': orig_handle.color,
            'fontproperties': fm.FontProperties(fname=FONTAWESOME_FILE, size=fontsize)
        }
        kwargs.update(orig_handle.kwargs)
        annotation = Text(x, y, orig_handle.text, **kwargs)
        return [annotation]


class Waffle(Figure):
    """

    A custom Figure class to make waffle charts.

    :param values: Numerical value of each category. If it is a dict, the keys would be used as labels.
    :type values: list|dict

    :param rows: The number of lines of the waffle chart. This is required if plots is not assigned.
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

    :param icon_legend: Whether to use icon but not color bar in legend. [Default False]
    :type icon_legend: bool

    :param interval_ratio_x: Ratio of distance between blocks on X to block's width. [Default 0.2]
    :type interval_ratio_x: float

    :param interval_ratio_y: Ratio of distance between blocks on Y to block's height. [Default 0.2]
    :type interval_ratio_y: float

    :param block_aspect: The ratio of block's width to height. [Default 1]
    :type block_aspect: float

    :param cmap_name: Name of colormaps for default color, if colors is not assigned.
        See full list in https://matplotlib.org/examples/color/colormaps_reference.html [Default 'Set2']
    :type cmap_name: str

    :param title: Parameters of matplotlib.axes.Axes.set_title in a dict.
        E.g. {'label': '', 'fontdict': {}, 'loc': ''}
        See full parameter list in https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_title.html
    :type title: dict

    :param icons: Icon name of Font Awesome. If it is a string, all categories use the same icon;
        If it's a list or tuple of icons, the length should be the same as values.
        See the full list of Font Awesome on http://fontawesome.io/icons/ [Default None]
    :type icons: str|list[str]|tuple[str]

    :param icon_size: Fint size of the icons. The default size is not fixed and depends on the block size.
    :type icon_size: int

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
        If a parameter of subplots is not assigned, it use the same parameter in Waffle class as default value.
    :type plots: dict
    """
    def __init__(self, *args, **kwargs):
        self.fig_args = {
            'values': kwargs.pop('values', []),
            'rows': kwargs.pop('rows', None),
            'columns': kwargs.pop('columns', None),
            'colors': kwargs.pop('colors', None),
            'labels': kwargs.pop('labels', None),
            'legend': kwargs.pop('legend', {}),
            'icon_legend': kwargs.pop('icon_legend', False),
            'interval_ratio_x': kwargs.pop('interval_ratio_x', 0.2),
            'interval_ratio_y': kwargs.pop('interval_ratio_y', 0.2),
            'block_aspect': kwargs.pop('block_aspect', 1),
            'cmap_name': kwargs.pop('cmap_name', 'Set2'),
            'title': kwargs.pop('title', None),
            'icons': kwargs.pop('icons', None),
            'icon_size': kwargs.pop('icon_size', None),
            'plot_anchor': kwargs.pop('plot_anchor', 'W'),
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

        if len(self._pa['values']) == 0 or not self._pa['rows']:
            raise ValueError("Argument values or rows is required.")

        # Append figure args to plot args
        plot_fig_args = copy.deepcopy(self.fig_args)
        for arg, v in plot_fig_args.items():
            if arg not in self._pa:
                self._pa[arg] = v

        self.values_len = len(self._pa['values'])

        if self._pa['colors'] and len(self._pa['colors']) != self.values_len:
            raise ValueError("Length of colors doesn't match the values.")

        if isinstance(self._pa['values'], dict):
            if not self._pa['labels']:
                self._pa['labels'] = self._pa['values'].keys()
            self._pa['values'] = list(self._pa['values'].values())

        if self._pa['labels'] and len(self._pa['labels']) != self.values_len:
            raise ValueError("Length of labels doesn't match the values.")

        if self._pa['icons']:
            from pywaffle.fontawesome_mapping import icons

            # If icons is a string, convert it into a list of same icon. It's length is the label's length
            # '\uf26e' -> ['\uf26e', '\uf26e', '\uf26e', ]
            if isinstance(self._pa['icons'], str):
                self._pa['icons'] = [self._pa['icons']] * self.values_len

            if len(self._pa['icons']) != self.values_len:
                raise ValueError("Length of icons doesn't match the values.")

            self._pa['icons'] = [icons[i] for i in self._pa['icons']]

        self.ax = self.add_subplot(loc, aspect='equal')

        # Alignment of subplots
        self.ax.set_anchor(self._pa['plot_anchor'])

        self.value_sum = float(sum(self._pa['values']))

        # if column number is not given, use the values as number of blocks
        if self._pa['columns'] is None:
            self._pa['columns'] = ceil(self.value_sum, self._pa['rows'])
            block_number_per_cat = self._pa['values']
        else:
            block_number_per_cat = [round(v * self._pa['columns'] * self._pa['rows'] / self.value_sum) for v in self._pa['values']]

        # Absolute height of the plot
        figure_height = 1
        block_y_length = figure_height / (self._pa['rows'] + self._pa['rows'] * self._pa['interval_ratio_y'] - self._pa['interval_ratio_y'])
        block_x_length = self._pa['block_aspect'] * block_y_length

        # Define the limit of X, Y axis
        self.ax.axis(
            xmin=0,
            xmax=(self._pa['columns'] + self._pa['columns'] * self._pa['interval_ratio_x'] - self._pa['interval_ratio_x']) * block_x_length,
            ymin=0,
            ymax=figure_height
        )

        # Default font size
        if self._pa['icons']:
            x, y = self.ax.transData.transform([(0, 0), (0, block_x_length)])
            prop = fm.FontProperties(
                fname=FONTAWESOME_FILE,
                size=self._pa['icon_size'] or int((y[1] - x[1]) / 16 * 12)
            )

        # Build a color sequence if colors is empty
        if not self._pa['colors']:
            default_colors = cm.get_cmap(self._pa['cmap_name']).colors
            default_color_num = cm.get_cmap(self._pa['cmap_name']).N
            self._pa['colors'] = array_resize(
                array=default_colors,
                length=self.values_len,
                array_len=default_color_num
            )

        # Plot blocks
        class_index = 0
        block_index = 0
        x_full = (1 + self._pa['interval_ratio_x']) * block_x_length
        y_full = (1 + self._pa['interval_ratio_y']) * block_y_length
        for col, row in unique_pairs(self._pa['columns'], self._pa['rows']):
            x = x_full * col
            y = y_full * row

            if self._pa['icons']:
                self.ax.text(
                    x=x,
                    y=y,
                    s=self._pa['icons'][class_index],
                    color=self._pa['colors'][class_index],
                    fontproperties=prop
                )
            else:
                self.ax.add_artist(
                    Rectangle(xy=(x, y), width=block_x_length, height=block_y_length,
                              color=self._pa['colors'][class_index])
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
            if self._pa['icons'] and self._pa['icon_legend']:
                self._pa['legend']['handles'] = [
                    TextLegend(color=c, text=i) for c, i in zip(self._pa['colors'], self._pa['icons'])
                ]
                self._pa['legend']['handler_map'] = {TextLegend: TextLegendHandler()}
            # elif not self._pa['legend'].get('handles'):
            elif 'handles' not in self._pa['legend']:
                self._pa['legend']['handles'] = [
                    Patch(color=c, label=str(l)) for c, l in zip(self._pa['colors'], self._pa['labels'])
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
