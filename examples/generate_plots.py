#!/usr/bin/python
# -*-coding: utf-8 -*-

# Run `python3 -m README_images.generate_plots` on root folder to generate plots for README

import matplotlib.pyplot as plt
from pywaffle.waffle import Waffle

# For README
readme_image_folder = 'examples/readme/'

# Basic
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 3])
fig.savefig(readme_image_folder + 'basic.svg', bbox_inches='tight')
plt.close(fig)

# Use values in dictionary; use absolute value as block number, without defining columns
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(FigureClass=Waffle, rows=5, values=data, legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)})
fig.savefig(readme_image_folder + 'absolute_block_numbers.svg', bbox_inches='tight')
plt.close(fig)

# Add title, legend, background color, block color and direction
# Data source https://en.wikipedia.org/wiki/United_States_presidential_election,_2016
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    colors=("#983D3D", "#232066", "#DCB732"),
    title={
        'label': 'Vote Percentage in 2016 US Presidential Election',
        'loc': 'left'
    },
    labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
    legend={
        'loc': 'lower left',
        'bbox_to_anchor': (0, -0.4),
        'ncol': len(data),
        'framealpha': 0
    },
    plot_direction='NW'
)
fig.savefig(readme_image_folder + 'title_and_legend.svg', bbox_inches='tight', facecolor='#EEEEEE')
plt.close(fig)

# Use icons from Awesomefont
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    colors=("#232066", "#983D3D", "#DCB732"),
    legend={
        'loc': 'upper left',
        'bbox_to_anchor': (1, 1)
    },
    icons='child',
    font_size=12,
    icon_legend=True
)
fig.savefig(readme_image_folder + 'fontawesome.svg', bbox_inches='tight')
plt.close(fig)

# Multiple Plots
import pandas as pd
data = pd.DataFrame(
    {
        'labels': ['Hillary Clinton', 'Donald Trump', 'Others'],
        'Virginia': [1981473, 1769443, 233715],
        'Maryland': [1677928, 943169, 160349],
        'West Virginia': [188794, 489371, 36258],
    },
).set_index('labels')

fig = plt.figure(
    FigureClass=Waffle,
    plots={
        '311': {
            'values': data['Virginia'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['Virginia'].items()],
            'legend': {
                'loc': 'upper left',
                'bbox_to_anchor': (1.05, 1),
                'fontsize': 8,
                'framealpha': 0
            },
            'title': {
                'label': '2016 Virginia Presidential Election Results',
                'loc': 'left'
            }
        },
        '312': {
            'values': data['Maryland'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['Maryland'].items()],
            'legend': {
                'loc': 'upper left',
                'bbox_to_anchor': (1.2, 1),
                'fontsize': 8,
                'framealpha': 0
            },
            'title': {
                'label': '2016 Maryland Presidential Election Results',
                'loc': 'left'
            }
        },
        '313': {
            'values': data['West Virginia'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['West Virginia'].items()],
            'legend': {
                'loc': 'upper left',
                'bbox_to_anchor': (1.3, 1),
                'fontsize': 8,
                'framealpha': 0
            },
            'title': {
                'label': '2016 West Virginia Presidential Election Results',
                'loc': 'left'
            }
        },
    },
    rows=5,
    colors=("#2196f3", "#ff5252", "#999999"),  # Default argument values for subplots
    figsize=(9, 5)  # figsize is a parameter of plt.figure
)
fig.savefig(readme_image_folder + 'multiple_plots.svg', bbox_inches='tight')
plt.close(fig)

# For documents
doc_examples_image_folder = 'examples/docs/'

# Basic
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 6])
fig.savefig(doc_examples_image_folder + 'basic_list_values.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values={
        'Cat1': 20,
        'Cat2': 12,
        'Cat3': 8
    },
    legend={
        'loc': 'upper left',
        'bbox_to_anchor': (1, 1)
    }
)
fig.savefig(doc_examples_image_folder + 'basic_dict_values.svg', bbox_inches='tight')
plt.close(fig)

# Value Scaling and Auto-columns
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 3], rounding_rule='floor')
fig.savefig(doc_examples_image_folder + 'value_scaling_and_auto_columns_rounding_rule.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[48, 46, 3])
fig.savefig(doc_examples_image_folder + 'value_scaling_and_auto_columns_ignore_columns.svg', bbox_inches='tight')
plt.close(fig)

# Title, Label and Legend
data = {'Cat1': 48, 'Cat2': 46, 'Cat3': 3}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=data,
    title={'label': 'Example plot', 'loc': 'left', 'fontdict': {'fontsize': 20}},
    labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.2), 'ncol': len(data), 'framealpha': 0, 'fontsize': 12}
)
fig.savefig(doc_examples_image_folder + 'title_label_ledend.svg', bbox_inches='tight')
plt.close(fig)

# Block Colors
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    colors=["#983D3D", "#232066", "#DCB732"]
)
fig.savefig(doc_examples_image_folder + 'block_colors.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    cmap_name="tab10"
)
fig.savefig(doc_examples_image_folder + 'block_colors_custom_cmap_name.svg', bbox_inches='tight')
plt.close(fig)

# Characters
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[48, 46, 3],
    colors=["#4c8cb5", "#b7cbd7", "#C0C0C0"],
    characters='⬤',
    font_size=12,
)
fig.savefig(doc_examples_image_folder + 'characters.svg', bbox_inches='tight')
plt.close(fig)

# Icons
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[48, 46, 3],
    colors=["#232066", "#983D3D", "#DCB732"],
    icons='star',
    font_size=12,
)
fig.savefig(doc_examples_image_folder + 'icons.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[48, 46, 3],
    colors=["#FFA500", "#4384FF", "#C0C0C0"],
    icons=['sun', 'cloud-showers-heavy', 'snowflake'],
    font_size=12,
    icon_style='solid',
    icon_legend=True,
    legend={'labels': ['sun', 'shower', 'snow'], 'loc': 'upper left', 'bbox_to_anchor': (1, 1)}
)
fig.savefig(doc_examples_image_folder + 'icons_different_per_category.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[48, 46, 3],
    colors=["#FFA500", "#4384FF", "#C0C0C0"],
    icons=['sun', 'cloud-showers-heavy', 'font-awesome-flag'],
    font_size=12,
    icon_style=['regular', 'solid', 'brands'],
    icon_legend=True,
    legend={'labels': ['sun', 'shower', 'flag'], 'loc': 'upper left', 'bbox_to_anchor': (1, 1)}
)
fig.savefig(doc_examples_image_folder + 'icons_different_style.svg', bbox_inches='tight')
plt.close(fig)

# Block shape, distance, location and direction
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    block_aspect_ratio=1.618,
)
fig.savefig(doc_examples_image_folder + 'block_shape.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    interval_ratio_x=1,
    interval_ratio_y=0.5
)
fig.savefig(doc_examples_image_folder + 'block_distance.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    starting_location='SE'
)
fig.savefig(doc_examples_image_folder + 'block_location.svg', bbox_inches='tight')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    vertical=True
)
fig.savefig(doc_examples_image_folder + 'block_direction.svg', bbox_inches='tight')
plt.close(fig)

# Adjust Figures
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    colors=["#983D3D", "#232066", "#DCB732"]
)
fig.set_facecolor('#DDDDDD')
fig.savefig(doc_examples_image_folder + 'adjust_figure_change_background.svg', bbox_inches='tight', facecolor='#DDDDDD')
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    plot_anchor='S'
)
fig.set_facecolor('#DDDDDD')
fig.savefig(doc_examples_image_folder + 'adjust_figure_location.svg', facecolor='#DDDDDD')
plt.close(fig)
