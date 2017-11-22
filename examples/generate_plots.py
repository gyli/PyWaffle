#!/usr/bin/python
# -*-coding: utf-8 -*-

# Run `python3 -m README_images.generate_plots` on root folder to generate plots for README

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle

image_folder = 'examples/'

# Basic
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 3])
fig.savefig(image_folder + 'basic.svg', bbox_inches='tight')


# Use values in dictionary; use absolute value as block number, without defining columns
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(FigureClass=Waffle, rows=5, values=data, legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)})
fig.savefig(image_folder + 'absolute_block_numbers.svg', bbox_inches='tight')


# Add title, legend and background color; and change block color
# Data source https://en.wikipedia.org/wiki/United_States_presidential_election,_2016
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle, rows=5, values=data,
    title_args={'label': 'Vote Percentage in 2016 US Presidential Election', 'loc': 'left'},
    colors=("#232066", "#983D3D", "#DCB732"),
    labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.4), 'ncol': len(data), 'framealpha': 0}
)
fig.gca().set_facecolor('#EEEEEE')
fig.set_facecolor('#EEEEEE')
plt.plot()
fig.savefig(image_folder + 'title_and_legend.svg', bbox_inches='tight', facecolor='#EEEEEE')


# Use icons from Awesomefont
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle, rows=5, values=data,
    colors=("#232066", "#983D3D", "#DCB732"),
    icons='child', icon_size=18,
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.05, 1)},
    icon_legend=True
)
fig.savefig(image_folder + 'fontawesome.svg', bbox_inches='tight')


# Multiple Plots
# https://www.census.gov/library/publications/2016/demo/p20-578.html
fig = plt.figure(
    FigureClass=Waffle, plots={
        '411': {'rows': 5, 'values': {"High school graduate or more": 43*0.9, "Below high school": 43*0.1}, 'legend': {'loc': 'upper left', 'bbox_to_anchor': (2, 1)}}

        ,'412': {'rows': 5, 'values': {"High school graduate or more": 40*0.88, "Below high school": 40*0.12}, 'legend': {'loc': 'upper left', 'bbox_to_anchor': (2, 1)}}
        # , 'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1)}
        ,'413': {'rows': 5, 'values': {"High school graduate or more": 83*0.89, "Below high school": 83*0.11}, 'legend': {'loc': 'upper left', 'bbox_to_anchor': (2, 1)}}
        # , 'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1)}
        ,'414': {'rows': 5, 'values': {"High school graduate or more": 46*0.89, "Below high school": 46*0.11}, 'legend': {'loc': 'upper left', 'bbox_to_anchor': (2, 1)}}
        # , 'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1)}
    }
)
fig.savefig(image_folder + 'multiple_plots.svg', bbox_inches='tight')
