#!/usr/bin/python
# -*-coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.font_manager as fm

prop = mpl.font_manager.FontProperties(fname='font/FontAwesome.otf')


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
    def __init__(self, height, values, *args, **kwargs):
        """
        custom kwarg figtitle is a figure title
        """
        width = kwargs.pop('width', None)
        colors = kwargs.pop('colors', None)
        interval_ratio_x = kwargs.pop('interval_ratio_x', 0.2)
        interval_ratio_y = kwargs.pop('interval_ratio_y', 0.2)
        width_height_ratio = kwargs.pop('width_height_ratio', 1)
        cmap_name = kwargs.pop('cmap_name', 'Set2')

        values_len = len(values)

        Figure.__init__(self, *args, **kwargs)

        value_sum = float(sum(values))

        # if width is not given, use the values as number of blocks
        value_as_block_number = False
        if width is None:
            width = ceil(value_sum, height)
            value_as_block_number = True

        self.ax = self.gca(aspect='equal')

        block_unit_value = width * height / value_sum
        block_numbers = values if value_as_block_number else [round(v * block_unit_value) for v in values]

        # Absolute height of the plot
        figure_height = 1

        block_height_length = figure_height / (height + height * interval_ratio_y - interval_ratio_y)
        block_width_length = width_height_ratio * block_height_length

        # Define the limit of X, Y axis
        self.ax.axis(
            [
                0, (width + width * interval_ratio_x - interval_ratio_x) * block_width_length,
                0, figure_height
            ]
        )

        # Build a color sequence with same length as values
        if colors:
            colors = array_resize(array=colors, length=values_len)
        else:
            default_colors = plt.cm.get_cmap(cmap_name).colors
            default_color_num = plt.cm.get_cmap(cmap_name).N
            colors = array_resize(array=default_colors, length=values_len, array_len=default_color_num)

        # Plot blocks
        class_index = 0
        block_index = 0
        for col, row in unique_pairs(width, height):
            self.ax.add_artist(
                Rectangle(
                    xy=(
                        (1 + interval_ratio_x) * block_width_length * col,
                        (1 + interval_ratio_y) * block_height_length * row
                    ),
                    width=block_width_length,
                    height=block_height_length,
                    color=colors[class_index]
                )
            )

            # ax.annotate('\uf2c6', (x, y), color='w', fontsize=32, fontproperties=prop)

            block_index += 1
            if block_index >= sum(block_numbers[:class_index + 1]):
                class_index += 1

                if class_index > values_len - 1:
                    break

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


fig = plt.figure(FigureClass=Waffle, height=4, values=[10, 20, 70], interval_ratio_x=0.2, colors=("#969696", "#1879bf", "#009bda"),
                 interval_ratio_y=0.2)
plt.show()
