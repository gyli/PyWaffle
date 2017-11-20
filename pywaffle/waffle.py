#!/usr/bin/python
# -*-coding: utf-8 -*-

from matplotlib.pyplot import cm
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Patch
import matplotlib.font_manager as fm
from matplotlib.text import Text
from matplotlib.legend_handler import HandlerBase


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


class TextLegend(object):
    def __init__(self, text, color, **kwargs):
        self.text = text
        self.color = color
        self.kwargs = kwargs


class TextLegendHandler(HandlerBase):
    def create_artists(self, legend, orig_handle, xdescent, ydescent,
                       width, height, fontsize, trans):
        x = xdescent + width / 2.0
        y = ydescent + height / 2.0
        kwargs = {
            'horizontalalignment': 'center',
            'verticalalignment': 'center',
            'color': orig_handle.color,
            'fontproperties': fm.FontProperties(fname='font/FontAwesome.otf', size=fontsize)
        }
        kwargs.update(orig_handle.kwargs)
        annotation = Text(x, y, orig_handle.text, **kwargs)
        return [annotation]


class Waffle(Figure):
    def __init__(self, *args, **kwargs):
        """
        custom kwarg figtitle is a figure title
        """
        self.fig_args = {
            'values': kwargs.pop('values', None),
            'rows': kwargs.pop('rows', None),
            'columns': kwargs.pop('columns', None),
            'colors': kwargs.pop('colors', None),
            'labels': kwargs.pop('labels', None),
            'legend_conf': kwargs.pop('legend_conf', {}),
            'icon_legend': kwargs.pop('icon_legend', False),
            'interval_ratio_x': kwargs.pop('interval_ratio_x', 0.2),
            'interval_ratio_y': kwargs.pop('interval_ratio_y', 0.2),
            'column_row_ratio': kwargs.pop('column_row_ratio', 1),
            'cmap_name': kwargs.pop('cmap_name', 'Set2'),
            'title_conf': kwargs.pop('title_conf', None),
            'icons': kwargs.pop('icons', None),
            'icon_size': kwargs.pop('icon_size', None)
        }
        self.plots = kwargs.pop('plots', None)

        if (self.fig_args['values'] is None or self.fig_args['rows'] is None) and self.plots is None:
            raise ValueError("Assign argument values and rows to build a single waffle chart or assign plots to build "
                             "multiple charts.")

        # If plots is empty, make a single waffle chart
        if self.plots is None:
            self.plots = {111: self.fig_args}

        Figure.__init__(self, *args, **kwargs)

        for loc, setting in self.plots.items():
            self._waffle(loc, **setting)

    def _waffle(self, loc, **kwargs):
        for k, v in self.fig_args.items():
            # Find args from plots first, if not found, use arguments of plt.figure
            value = kwargs[k] if k in kwargs.keys() else v
            # Update the attributes
            self.__setattr__(k, value)

        self.values_len = len(self.values)

        if self.colors and len(self.colors) != self.values_len:
            raise ValueError("Length of colors doesn't match the values.")

        if isinstance(self.values, dict):
            if not self.labels:
                self.labels = self.values.keys()
            self.values = list(self.values.values())

        if self.labels and len(self.labels) != self.values_len:
            raise ValueError("Length of labels doesn't match the values.")

        if self.icons:
            from pywaffle.awesomefont_mapping import af_mapping
            if isinstance(self.icons, str):
                self.icons = [self.icons] * self.values_len
            if len(self.icons) != self.values_len:
                raise ValueError("Length of icons doesn't match the values.")
            self.icons = [af_mapping[i] for i in self.icons]

        # default legend_conf
        self.legend_conf = dict({'loc': (0, -0.1), 'ncol': self.values_len}, **self.legend_conf)

        self.ax = self.add_subplot(loc, aspect='equal')

        self.value_sum = float(sum(self.values))

        # if column number is not given, use the values as number of blocks
        self.value_as_block_number = False
        if self.columns is None:
            self.columns = ceil(self.value_sum, self.rows)
            self.value_as_block_number = True

        block_unit_value = self.columns * self.rows / self.value_sum
        block_numbers = self.values if self.value_as_block_number else [round(v * block_unit_value) for v in self.values]

        # Absolute height of the plot
        figure_height = 1

        block_y_length = figure_height / (self.rows + self.rows * self.interval_ratio_y - self.interval_ratio_y)
        block_x_length = self.column_row_ratio * block_y_length

        # Define the limit of X, Y axis
        self.ax.axis(
            xmin=0, xmax=(self.columns + self.columns * self.interval_ratio_x - self.interval_ratio_x) * block_x_length,
            ymin=0, ymax=figure_height
        )

        # Default font size
        if self.icons:
            x, y = self.ax.transData.transform([(0, 0), (0, block_x_length)])
            prop = fm.FontProperties(fname='font/FontAwesome.otf', size=self.icon_size or int((y[1] - x[1]) / 16 * 12))

        # Build a color sequence if colors is empty
        if not self.colors:
            default_colors = cm.get_cmap(self.cmap_name).colors
            default_color_num = cm.get_cmap(self.cmap_name).N
            self.colors = array_resize(array=default_colors, length=self.values_len, array_len=default_color_num)

        # Plot blocks
        class_index = 0
        block_index = 0
        unique_class_index = []
        unique_class_items = []
        for col, row in unique_pairs(self.columns, self.rows):
            if self.icons:
                item = self.ax.text(
                    x=(1 + self.interval_ratio_x) * block_x_length * col,
                    y=(1 + self.interval_ratio_y) * block_y_length * row,
                    s=self.icons[class_index],
                    color=self.colors[class_index],
                    fontproperties=prop
                )
            else:
                item = Rectangle(
                    xy=(
                        (1 + self.interval_ratio_x) * block_x_length * col,
                        (1 + self.interval_ratio_y) * block_y_length * row
                    ),
                    width=block_x_length,
                    height=block_y_length,
                    color=self.colors[class_index],
                )
                self.ax.add_artist(item)

            # Build a list of unique_class_items for legend
            if class_index not in unique_class_index:
                unique_class_items.append(item)
                unique_class_index.append(class_index)

            block_index += 1
            if block_index >= sum(block_numbers[:class_index + 1]):
                class_index += 1

                if class_index > self.values_len - 1:
                    break

        # Add title
        if self.title_conf is not None:
            self.ax.set_title(**self.title_conf)

        # Add legend
        if self.icons and self.icon_legend:
            # self.legend_conf['handles'] = unique_class_items
            self.legend_conf['handles'] = [TextLegend(color=self.colors[i], text=l) for i, l in enumerate(self.icons)]
            self.legend_conf['handler_map'] = {TextLegend: TextLegendHandler()}
        elif not self.legend_conf.get('handles'):
            self.legend_conf['handles'] = [Patch(color=self.colors[i], label=str(l)) for i, l in enumerate(self.labels)]

        # labels is an alias of legend_conf['labels']
        if 'labels' not in self.legend_conf and self.labels:
            self.legend_conf['labels'] = self.labels

        if self.legend_conf['labels'] or self.legend_conf['handles']:
            self.ax.legend(**self.legend_conf)

        # Remove borders, ticks, etc.
        self.ax.axis('off')

    def remove(self):
        pass
