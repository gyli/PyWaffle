#!/usr/bin/python
# -*-coding: utf-8 -*-

# Run `python3 -m README_images.generate_plots` on root folder to generate plots for README

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle


image_folder = 'README_images/'

# Basic
fig = plt.figure(FigureClass=Waffle, rows=3, columns=10, values=[30, 20, 10])
fig.savefig(image_folder + 'basic.png', bbox_inches='tight', dpi=200)


# Use values in dictionary; use absolute value as block number, without defining columns
fig = plt.figure(FigureClass=Waffle, rows=6, values={'Cat1': 35, 'Cat2': 24, 'Cat3': 9},
                 legend_args={'loc': (0, -0.15)})
fig.savefig(image_folder + 'absolute_block_numbers.png', bbox_inches='tight', dpi=200)


# Add title, legend and background color; and change block color
fig = plt.figure(FigureClass=Waffle, rows=6, values={'Cat1': 35, 'Cat2': 24, 'Cat3': 9},
                 colors=("#FCF8C1", "#CEEEF9", "#E9DBF9"),
                 title_args={'label': 'Here is the title', 'loc': 'left'},
                 legend_args={'loc': (0, -0.15), 'facecolor': '#EEEEEE'})
fig.gca().set_facecolor('#EEEEEE')
fig.set_facecolor('#EEEEEE')
fig.savefig(image_folder + 'title_and_legend.png', bbox_inches='tight', dpi=200, facecolor='#EEEEEE')

