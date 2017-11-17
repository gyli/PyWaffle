#!/usr/bin/python
# -*-coding: utf-8 -*-

# python3 -m README_images.generate_plots

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle


image_folder = 'README_images/'

# Basic
fig = plt.figure(FigureClass=Waffle, rows=6, columns=10, values=[30, 20, 10])
fig.savefig(image_folder + 'basic.png', bbox_inches='tight', dpi=200)


# Absolute block number and value in dict
fig = plt.figure(FigureClass=Waffle, rows=6, values={'Cat1': 35, 'Cat2': 24, 'Cat3': 9},
                 legend_args={'loc': (0, -0.15)})
fig.savefig(image_folder + 'absolute_block_numbers.png', bbox_inches='tight', dpi=200)

# Add title, legend and background color
fig = plt.figure(FigureClass=Waffle, rows=6, values={'Cat1': 35, 'Cat2': 24, 'Cat3': 9},
                 title_args={'label': 'Here is the title', 'loc': 'left'},
                 legend_args={'loc': (0, -0.15), 'facecolor': '#EAEAEA'})
fig.gca().set_facecolor('#EAEAEA')
fig.set_facecolor('#EAEAEA')
fig.savefig(image_folder + 'title_and_legend.png', bbox_inches='tight', dpi=200, facecolor='#EAEAEA')

