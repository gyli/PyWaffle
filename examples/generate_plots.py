#!/usr/bin/python
# -*-coding: utf-8 -*-

# Run `python3 -m README_images.generate_plots` on root folder to generate plots for README

import matplotlib.pyplot as plt

from pywaffle.waffle import Waffle

# For README
readme_image_folder = "examples/readme/"

# Basic
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 6], figsize=(5, 3))
fig.savefig(readme_image_folder + "basic.svg", bbox_inches="tight")
plt.close(fig)

# Use values in dictionary; use absolute value as block number, without defining columns
data = {"Cat1": 10, "Cat2": 7, "Cat3": 9}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
)
fig.savefig(readme_image_folder + "absolute_block_numbers.svg", bbox_inches="tight")
plt.close(fig)

# Add title, legend, background color, block color, direction and style
data = {'Car': 58, 'Pickup': 21, 'Truck': 11, 'Motorcycle': 7}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    colors=["#c1d82f", "#00a4e4", "#fbb034", '#6a737b'],
    title={'label': 'Vehicle Sales by Vehicle Type', 'loc': 'left'},
    labels=[f"{k} ({v}%)" for k, v in data.items()],
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.4), 'ncol': len(data), 'framealpha': 0},
    starting_location='NW',
    vertical=True,
    block_arranging_style='snake'
)
fig.savefig(readme_image_folder + "title_and_legend.svg", bbox_inches="tight", facecolor="#EEEEEE")
plt.close(fig)

# Use icons from Font Awesome
data = {'Car': 58, 'Pickup': 21, 'Truck': 11, 'Motorcycle': 7}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    colors=["#c1d82f", "#00a4e4", "#fbb034", '#6a737b'],
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)},
    icons=['car-side', 'truck-pickup', 'truck', 'motorcycle'],
    font_size=12,
    icon_legend=True
)
fig.savefig(readme_image_folder + "fontawesome.svg", bbox_inches="tight")
plt.close(fig)

# plotting on existed figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Modify existed axis
ax.set_title("Axis Title")
ax.set_aspect(aspect="equal")

Waffle.make_waffle(
    ax=ax,  # pass axis to make_waffle
    rows=5,
    columns=10,
    values=[30, 16, 4],
    title={"label": "Waffle Title", "loc": "left"}
)
fig.savefig(readme_image_folder + "existed_axis.svg", bbox_inches="tight")
plt.close(fig)

# Multiple Plots
import pandas as pd

data = pd.DataFrame(
    {
        'labels': ['Car', 'Truck', 'Motorcycle'],
        'Factory A': [32384, 13354, 5245],
        'Factory B': [22147, 6678, 2156],
        'Factory C': [8932, 3879, 896],
    },
).set_index('labels')

fig = plt.figure(
    FigureClass=Waffle,
    plots={
        311: {
            'values': data['Factory A'] / 1000,  # Convert actual number to a reasonable block number
            'labels': [f"{k} ({v})" for k, v in data['Factory A'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1), 'fontsize': 8},
            'title': {'label': 'Vehicle Production of Factory A', 'loc': 'left', 'fontsize': 12}
        },
        312: {
            'values': data['Factory B'] / 1000,
            'labels': [f"{k} ({v})" for k, v in data['Factory B'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.2, 1), 'fontsize': 8},
            'title': {'label': 'Vehicle Production of Factory B', 'loc': 'left', 'fontsize': 12}
        },
        313: {
            'values': data['Factory C'] / 1000,
            'labels': [f"{k} ({v})" for k, v in data['Factory C'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.3, 1), 'fontsize': 8},
            'title': {'label': 'Vehicle Production of Factory C', 'loc': 'left', 'fontsize': 12}
        },
    },
    rows=5,  # Outside parameter applied to all subplots, same as below
    cmap_name="Accent",  # Change color with cmap
    rounding_rule='ceil',  # Change rounding rule, so value less than 1000 will still have at least 1 block
    figsize=(5, 5)
)
fig.suptitle('Vehicle Production by Vehicle Type', fontsize=14, fontweight='bold')
fig.supxlabel('1 block = 1000 vehicles', fontsize=8, ha='right')
fig.set_facecolor('#EEEDE7')
fig.savefig(readme_image_folder + "multiple_plots.svg", bbox_inches="tight")
plt.close(fig)

# For documents
doc_examples_image_folder = "examples/docs/"

# Basic
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 16, 4])
fig.savefig(doc_examples_image_folder + "basic_list_values.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values={"Cat1": 30, "Cat2": 16, "Cat3": 4},
    legend={"loc": "upper left", "bbox_to_anchor": (1, 1)},
)
fig.savefig(doc_examples_image_folder + "basic_dict_values.svg", bbox_inches="tight")
plt.close(fig)

# Plot on Existed Axis
fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_title("Axis Title")
ax.set_aspect(aspect="equal")

Waffle.make_waffle(ax=ax, rows=5, columns=10, values=[30, 16, 4], title={"label": "Waffle Title", "loc": "left"})
fig.savefig(doc_examples_image_folder + "plot_on_existed_axis.svg", bbox_inches="tight")

# Value Scaling and Auto-sizing
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 3], rounding_rule="floor")
fig.savefig(doc_examples_image_folder + "value_scaling_and_auto_sizing_rounding_rule.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[48, 46, 3])
fig.savefig(doc_examples_image_folder + "value_scaling_and_auto_sizing_ignore_columns.svg", bbox_inches="tight")
plt.close(fig)

# Title, Label and Legend
data = {"Cat1": 30, "Cat2": 16, "Cat3": 4}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=data,
    title={"label": "Example plot", "loc": "left", "fontdict": {"fontsize": 20}},
    labels=[f"{k} ({int(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
    legend={"loc": "lower left", "bbox_to_anchor": (0, -0.2), "ncol": len(data), "framealpha": 0, "fontsize": 12},
)
fig.savefig(doc_examples_image_folder + "title_label_ledend.svg", bbox_inches="tight")
plt.close(fig)

# Block Colors
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 16, 4], colors=["#232066", "#983D3D", "#DCB732"])
fig.savefig(doc_examples_image_folder + "block_colors.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[30, 16, 4], cmap_name="tab10")
fig.savefig(doc_examples_image_folder + "block_colors_custom_cmap_name.svg", bbox_inches="tight")
plt.close(fig)

# Characters
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    colors=["#4c8cb5", "#b7cbd7", "#C0C0C0"],
    characters="⬤",
    font_size=24,
)
fig.savefig(doc_examples_image_folder + "characters.svg", bbox_inches="tight")
plt.close(fig)

# Icons
fig = plt.figure(
    FigureClass=Waffle, rows=5, values=[30, 16, 4], colors=["#232066", "#983D3D", "#DCB732"], icons="star", font_size=24
)
fig.savefig(doc_examples_image_folder + "icons.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    colors=["#FFA500", "#4384FF", "#C0C0C0"],
    icons=["sun", "cloud-showers-heavy", "snowflake"],
    font_size=20,
    icon_style="solid",
    icon_legend=True,
    legend={"labels": ["sun", "shower", "snow"], "loc": "upper left", "bbox_to_anchor": (1, 1)},
)
fig.savefig(doc_examples_image_folder + "icons_different_per_category.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    colors=["#FFA500", "#4384FF", "#C0C0C0"],
    icons=["sun", "cloud-showers-heavy", "font-awesome"],
    font_size=20,
    icon_style=["regular", "solid", "brands"],
    icon_legend=True,
    legend={"labels": ["sun", "shower", "flag"], "loc": "upper left", "bbox_to_anchor": (1, 1)},
)
fig.savefig(doc_examples_image_folder + "icons_different_style.svg", bbox_inches="tight")
plt.close(fig)

# Block shape, distance, location and direction
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    block_aspect_ratio=1.618,
)
fig.savefig(doc_examples_image_folder + "block_shape.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[30, 16, 4], interval_ratio_x=1, interval_ratio_y=0.5)
fig.savefig(doc_examples_image_folder + "block_distance.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[30, 16, 4], starting_location="SE")
fig.savefig(doc_examples_image_folder + "block_location.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[12, 22, 20, 4], block_arranging_style="snake")
fig.savefig(doc_examples_image_folder + "snake_pattern.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, columns=10, values=[30, 16, 4], block_arranging_style="new-line", vertical=True)
fig.savefig(doc_examples_image_folder + "new_line_pattern.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[30, 16, 4], vertical=True)
fig.savefig(doc_examples_image_folder + "block_direction.svg", bbox_inches="tight")
plt.close(fig)

# Adjust Figures
fig = plt.figure(
    FigureClass=Waffle, rows=5, values=[30, 16, 4], colors=["#232066", "#983D3D", "#DCB732"], facecolor="#DDDDDD"
)
fig.savefig(doc_examples_image_folder + "adjust_figure_change_background.svg", bbox_inches="tight", facecolor="#DDDDDD")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[30, 16, 4], plot_anchor="S", facecolor="#DDDDDD")
fig.savefig(doc_examples_image_folder + "adjust_figure_location.svg", facecolor="#DDDDDD")
plt.close(fig)

fig = plt.figure(FigureClass=Waffle, rows=5, values=[30, 16, 4])
fig.text(
    x=0.5,
    y=0.5,
    s="Sample",
    ha="center",
    va="center",
    rotation=30,
    fontsize=40,
    color="gray",
    alpha=0.3,
    bbox={"boxstyle": "square", "lw": 3, "ec": "gray", "fc": (0.9, 0.9, 0.9, 0.5), "alpha": 0.3},
)
fig.savefig(doc_examples_image_folder + "add_other_elements.svg", bbox_inches="tight")
plt.close(fig)
