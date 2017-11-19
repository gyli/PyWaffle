#!/usr/bin/python
# -*-coding: utf-8 -*-

# Run `python3 -m README_images.generate_plots` on root folder to generate plots for README

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle

image_folder = 'README_images/'

# Basic
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 3])
fig.savefig(image_folder + 'basic.svg', bbox_inches='tight')


# Use values in dictionary; use absolute value as block number, without defining columns
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(FigureClass=Waffle, rows=5, values=data, legend_conf={'loc': (0, -0.3)})
fig.savefig(image_folder + 'absolute_block_numbers.svg', bbox_inches='tight')


# Add title, legend and background color; and change block color
# Data source https://en.wikipedia.org/wiki/United_States_presidential_election,_2016
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle, rows=5, values=data,
    title_conf={'label': 'Vote Percentage in 2016 US Presidential Election', 'loc': 'left'},
    colors=("#232066", "#983D3D", "#DCB732"),
    labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
    legend_conf={'loc': (0, -0.3), 'fontsize': 10, 'framealpha': 0}
)
fig.gca().set_facecolor('#EEEEEE')
fig.set_facecolor('#EEEEEE')
plt.plot()
fig.savefig(image_folder + 'title_and_legend.svg', bbox_inches='tight', facecolor='#EEEEEE')


# Use icons from Awesomefont
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle, rows=5, values=data, legend_conf={'loc': (0, -0.3)},
    colors=("#232066", "#983D3D", "#DCB732"),
    icons='child', icon_size=18, interval_ratio_y=0.3,

)
fig.savefig(image_folder + 'fontawesome.svg', bbox_inches='tight')
