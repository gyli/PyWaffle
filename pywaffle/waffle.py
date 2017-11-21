#!/usr/bin/python
# -*-coding: utf-8 -*-

from matplotlib.pyplot import cm
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Patch
import matplotlib.font_manager as fm
from matplotlib.text import Text
from matplotlib.legend_handler import HandlerBase
import copy


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


FONTAWESOME_FILE = 'font/FontAwesome.otf'


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
            'legend_args': kwargs.pop('legend_args', {}),
            'icon_legend': kwargs.pop('icon_legend', False),
            'interval_ratio_x': kwargs.pop('interval_ratio_x', 0.2),
            'interval_ratio_y': kwargs.pop('interval_ratio_y', 0.2),
            'column_row_ratio': kwargs.pop('column_row_ratio', 1),
            'cmap_name': kwargs.pop('cmap_name', 'Set2'),
            'title_conf': kwargs.pop('title_conf', None),
            'icons': kwargs.pop('icons', None),
            'icon_size': kwargs.pop('icon_size', None),
            'plot_anchor': kwargs.pop('plot_anchor', 'W')
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
        # pargs is the arguments for this single plot
        self.pargs = kwargs

        # Append figure args to plot args
        plot_fig_args = copy.deepcopy(self.fig_args)
        for arg, v in plot_fig_args.items():
            if arg not in self.pargs:
                self.pargs[arg] = v

        self.values_len = len(self.pargs['values'])

        if self.pargs['colors'] and len(self.pargs['colors']) != self.values_len:
            raise ValueError("Length of colors doesn't match the values.")

        if isinstance(self.pargs['values'], dict):
            if not self.pargs['labels']:
                self.pargs['labels'] = self.pargs['values'].keys()
            self.pargs['values'] = list(self.pargs['values'].values())

        if self.pargs['labels'] and len(self.pargs['labels']) != self.values_len:
            raise ValueError("Length of labels doesn't match the values.")

        if self.pargs['icons']:
            from pywaffle.awesomefont_mapping import af_mapping
            # If icons is a string, convert it into a list of same icon. It's length is the label's length
            # '\uf26e' -> ['\uf26e', '\uf26e', '\uf26e', ]
            if isinstance(self.pargs['icons'], str):
                self.pargs['icons'] = [self.pargs['icons']] * self.values_len
            if len(self.pargs['icons']) != self.values_len:
                raise ValueError("Length of icons doesn't match the values.")
            self.pargs['icons'] = [af_mapping[i] for i in self.pargs['icons']]

        self.ax = self.add_subplot(loc, aspect='equal')

        # Alignment of subplots
        self.ax.set_anchor(self.pargs['plot_anchor'])

        self.value_sum = float(sum(self.pargs['values']))

        # if column number is not given, use the values as number of blocks
        self.value_as_block_number = False
        if self.pargs['columns'] is None:
            self.pargs['columns'] = ceil(self.value_sum, self.pargs['rows'])
            self.value_as_block_number = True

        block_unit_value = self.pargs['columns'] * self.pargs['rows'] / self.value_sum
        block_numbers = self.pargs['values'] if self.value_as_block_number else [round(v * block_unit_value) for v in self.pargs['values']]

        # Absolute height of the plot
        figure_height = 1

        block_y_length = figure_height / (self.pargs['rows'] + self.pargs['rows'] * self.pargs['interval_ratio_y'] - self.pargs['interval_ratio_y'])
        block_x_length = self.pargs['column_row_ratio'] * block_y_length

        # Define the limit of X, Y axis
        self.ax.axis(
            xmin=0, xmax=(self.pargs['columns'] + self.pargs['columns'] * self.pargs['interval_ratio_x'] - self.pargs['interval_ratio_x']) * block_x_length,
            ymin=0, ymax=figure_height
        )

        # Default font size
        if self.pargs['icons']:
            x, y = self.ax.transData.transform([(0, 0), (0, block_x_length)])
            prop = fm.FontProperties(fname=FONTAWESOME_FILE, size=self.pargs['icon_size'] or int((y[1] - x[1]) / 16 * 12))

        # Build a color sequence if colors is empty
        if not self.pargs['colors']:
            default_colors = cm.get_cmap(self.pargs['cmap_name']).colors
            default_color_num = cm.get_cmap(self.pargs['cmap_name']).N
            self.pargs['colors'] = array_resize(array=default_colors, length=self.values_len, array_len=default_color_num)

        # Plot blocks
        class_index = 0
        block_index = 0
        unique_class_index = []
        unique_class_items = []
        for col, row in unique_pairs(self.pargs['columns'], self.pargs['rows']):
            x = (1 + self.pargs['interval_ratio_x']) * block_x_length * col
            y = (1 + self.pargs['interval_ratio_y']) * block_y_length * row
            if self.pargs['icons']:
                item = self.ax.text(x=x, y=y, s=self.pargs['icons'][class_index], color=self.pargs['colors'][class_index],
                                    fontproperties=prop)
            else:
                item = Rectangle(xy=(x, y), width=block_x_length, height=block_y_length, color=self.pargs['colors'][class_index])
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
        if self.pargs['title_conf'] is not None:
            self.ax.set_title(**self.pargs['title_conf'])

        # Add legend
        if self.pargs['labels'] or 'labels' in self.pargs['legend_args']:
            if self.pargs['icons'] and self.pargs['icon_legend']:
                # self.plot_args['legend_args']['handles'] = unique_class_items
                self.pargs['legend_args']['handles'] = [TextLegend(color=self.pargs['colors'][i], text=l) for i, l in enumerate(self.pargs['icons'])]
                self.pargs['legend_args']['handler_map'] = {TextLegend: TextLegendHandler()}
            elif not self.pargs['legend_args'].get('handles'):
                self.pargs['legend_args']['handles'] = [Patch(color=self.pargs['colors'][i], label=str(l)) for i, l in enumerate(self.pargs['labels'])]

            # labels is an alias of legend['labels']
            if 'labels' not in self.pargs['legend_args'] and self.pargs['labels']:
                self.pargs['legend_args']['labels'] = self.pargs['labels']

            if 'handles' in self.pargs['legend_args'] and 'labels' in self.pargs['legend_args']:
                self.ax.legend(**self.pargs['legend_args'])

        # Remove borders, ticks, etc.
        self.ax.axis('off')

    def remove(self):
        pass
