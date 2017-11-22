#!/usr/bin/python
# -*-coding: utf-8 -*-

# Run `python3 -m README_images.generate_plots` on root folder to generate plots for README

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle

image_folder = 'examples/'

# Basic
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3]
)
fig.savefig(image_folder + 'basic.svg', bbox_inches='tight')


# Use values in dictionary; use absolute value as block number, without defining columns
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)}
)
fig.savefig(image_folder + 'absolute_block_numbers.svg', bbox_inches='tight')


# Add title, legend and background color; and change block color
# Data source https://en.wikipedia.org/wiki/United_States_presidential_election,_2016
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    colors=("#983D3D", "#232066", "#DCB732"),
    title={'label': 'Vote Percentage in 2016 US Presidential Election', 'loc': 'left'},
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
    FigureClass=Waffle,
    rows=5,
    values=data,
    colors=("#232066", "#983D3D", "#DCB732"),
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)},
    icons='child', icon_size=18,
    icon_legend=True
)
fig.savefig(image_folder + 'fontawesome.svg', bbox_inches='tight')


# Multiple Plots
import pandas as pd
data = pd.DataFrame(
    {
        'labels': ['Hillary Clinton', 'Donald Trump', 'Others'],
        'Virginia': [1916845, 1731156, 196786],
        'Maryland': [1497951, 873646, 102946],
        'West Virginia': [187457, 486198, 27371],
    },
).set_index('labels')

fig = plt.figure(
    FigureClass=Waffle,
    plots={
        '311': {
            'values': data['Virginia'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['Virginia'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1), 'fontsize': 8, 'framealpha': 0},
            'title': {'label': '2016 Virginia Presidential Election Results', 'loc': 'left'}
        },
        '312': {
            'values': data['Maryland'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['Maryland'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.2, 1), 'fontsize': 8, 'framealpha': 0},
            'title': {'label': '2016 Maryland Presidential Election Results', 'loc': 'left'}
        },
        '313': {
            'values': data['West Virginia'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['West Virginia'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.3, 1), 'fontsize': 8, 'framealpha': 0},
            'title': {'label': '2016 West Virginia Presidential Election Results', 'loc': 'left'}
        },
    },
    rows=5,
    colors=("#232066", "#983D3D", "#999999"),  # Default argument values for subplots
    figsize=(9, 5)  # figsize is a parameter of plt.figure
)
# https://www.politico.com/2016-election/results/map/president/
fig.savefig(image_folder + 'multiple_plots.svg', bbox_inches='tight')
