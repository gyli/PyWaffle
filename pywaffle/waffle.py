#!/usr/bin/python
# -*-coding: utf-8 -*-

from matplotlib.pyplot import cm
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Patch
import matplotlib.font_manager as fm

prop = fm.FontProperties(fname='font/FontAwesome.otf')


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


class Waffle(Figure):
    def __init__(self, rows, values, *args, **kwargs):
        """
        custom kwarg figtitle is a figure title
        """
        columns = kwargs.pop('columns', None)
        colors = kwargs.pop('colors', None)
        labels = kwargs.pop('labels', None)
        legend_args = kwargs.pop('legend_args', {})
        interval_ratio_x = kwargs.pop('interval_ratio_x', 0.2)
        interval_ratio_y = kwargs.pop('interval_ratio_y', 0.2)
        column_row_ratio = kwargs.pop('column_row_ratio', 1)
        cmap_name = kwargs.pop('cmap_name', 'Set2')
        title_args = kwargs.pop('title_args', None)

        values_len = len(values)

        if colors and len(colors) != values_len:
            raise ValueError("Length of colors doesn't match the values.")

        if isinstance(values, dict):
            if not labels:
                labels = values.keys()
            values = list(values.values())

        if labels and len(labels) != values_len:
            raise ValueError("Length of labels doesn't match the values.")

        # default legend_args
        legend_args = dict({'loc': (0, -0.1), 'ncol': values_len}, **legend_args)

        Figure.__init__(self, *args, **kwargs)

        value_sum = float(sum(values))

        # if column number is not given, use the values as number of blocks
        value_as_block_number = False
        if columns is None:
            columns = ceil(value_sum, rows)
            value_as_block_number = True

        self.ax = self.gca(aspect='equal')

        block_unit_value = columns * rows / value_sum
        block_numbers = values if value_as_block_number else [round(v * block_unit_value) for v in values]

        # Absolute height of the plot
        figure_height = 1

        block_y_length = figure_height / (rows + rows * interval_ratio_y - interval_ratio_y)
        block_x_length = column_row_ratio * block_y_length

        # Define the limit of X, Y axis
        self.ax.axis(
            [
                0, (columns + columns * interval_ratio_x - interval_ratio_x) * block_x_length,
                0, figure_height
            ]
        )

        # Build a color sequence if colors is empty
        if not colors:
            default_colors = cm.get_cmap(cmap_name).colors
            default_color_num = cm.get_cmap(cmap_name).N
            colors = array_resize(array=default_colors, length=values_len, array_len=default_color_num)

        # Plot blocks
        class_index = 0
        block_index = 0
        for col, row in unique_pairs(columns, rows):
            self.ax.add_artist(
                Rectangle(
                    xy=(
                        (1 + interval_ratio_x) * block_x_length * col,
                        (1 + interval_ratio_y) * block_y_length * row
                    ),
                    width=block_x_length,
                    height=block_y_length,
                    color=colors[class_index],
                )
            )

            # ax.annotate('\uf2c6', (x, y), color='w', fontsize=32, fontproperties=prop)

            block_index += 1
            if block_index >= sum(block_numbers[:class_index + 1]):
                class_index += 1

                if class_index > values_len - 1:
                    break

        # Add title
        if title_args is not None:
            self.ax.set_title(**title_args)

        # Add legend
        if labels is not None:
            self.ax.legend(handles=[Patch(color=colors[i], label=str(l)) for i, l in enumerate(labels)], **legend_args)

        # Remove unnecessary lines, ticks, etc.
        self.ax.tick_params(
            axis='both',
            which='both',
            bottom=False,
            left=False,
            top=False,
            labelbottom=False,
            labelleft=False
        )

        for spine in self.ax.spines.values():
            spine.set_visible(False)

    def remove(self):
        pass
