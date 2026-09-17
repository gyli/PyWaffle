#!/usr/bin/python
# -*-coding: utf-8 -*-

# Run `python3 -m examples.generate_plots` from the repository root to regenerate the images
# used by the README and the documentation.

import matplotlib.pyplot as plt

from pywaffle import waffle_chart
from pywaffle.waffle import Waffle

# For README
readme_image_folder = "examples/readme/"

# Basic
fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 6], figsize=(5, 3))
fig.savefig(readme_image_folder + "basic.svg", bbox_inches="tight")
plt.close(fig)

# Use values in dictionary; use absolute value as block number, without defining columns
data = {'Cat1': 40, 'Cat2': 27, 'Cat3': 9}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.05, 1)}
)
fig.savefig(readme_image_folder + "absolute_block_numbers.svg", bbox_inches="tight")
plt.close(fig)

# Add title, legend, background color, block color, direction and style
data = {'Car': 58, 'Pickup': 21, 'Truck': 11, 'Motorcycle': 7}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    colors=["#C1D82F", "#00A4E4", "#FBB034", '#6A737B'],
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
    figsize=(6, 5)
)
fig.suptitle('Vehicle Production by Vehicle Type', fontsize=14, fontweight='bold')
fig.supxlabel('1 block = 1000 vehicles', fontsize=8, x=0.14)
fig.set_facecolor('#EEEDE7')
fig.savefig(readme_image_folder + "multiple_plots.svg")
plt.close(fig)

# For documents
doc_examples_image_folder = "examples/docs/"

# Formats of values
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

# Figure and Axis manipulation
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

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values={"Net income": 18.46, "Income tax": 1.64, "MG&A": 7.52, "R&D": 15.3, "Cost of sales": 44.54},
    rounding_rule="float",
    block_arranging_style="snake",
    legend={"loc": "lower left", "bbox_to_anchor": (0, -0.6), "ncol": 2, "framealpha": 0},
)
fig.savefig(doc_examples_image_folder + "value_scaling_and_auto_sizing_fractional.svg", bbox_inches="tight")
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

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[30, 16, 4],
    background_color="#2b2b2b",
)
fig.savefig(doc_examples_image_folder + "block_background_color.svg", bbox_inches="tight")
plt.close(fig)

fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[30, 16, 4],
    interval_ratio_x=0,
    interval_ratio_y=0,
    block_edge_color="white",
    block_edge_width=1.5,
)
fig.savefig(doc_examples_image_folder + "block_edge_color.svg", bbox_inches="tight")
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


# ---------------------------------------------------------------------------
# Quickstart
#
# One dataset carried through the whole quickstart, so that each chart adds a
# single idea rather than restarting on new numbers. It is a real dataset, which
# is the point: a waffle chart's argument is that one block is one real thing.
#
# These calls are written exactly as docs/quickstart.md shows them, so the code a
# reader copies is the code that produced the image underneath it.
#
# Source: British Board of Trade inquiry (1912) into the loss of the RMS Titanic.
#         2,201 aboard, 710 saved, 1,491 lost. Tabulated at
#         https://en.wikipedia.org/wiki/Sinking_of_the_Titanic#Casualties_and_survivors
#
# A 1912 inquiry cannot go out of date, so unlike a yearly statistic these numbers
# never need refreshing. Class totals are the sum of the men, women and children
# rows of that table, and are consistent with its published totals.
# ---------------------------------------------------------------------------
quickstart_image_folder = "examples/quickstart/"

aboard = {"First class": 325, "Second class": 285, "Third class": 706, "Crew": 885}
by_group = {"Men": 1667, "Women": 425, "Children": 109}
saved = {"First class": 202, "Second class": 118, "Third class": 178, "Crew": 212}

class_colors = ["#c9a227", "#5f8a8b", "#b5653f", "#3d4f5d"]
group_colors = ["#3d4f5d", "#c9a227", "#b5653f"]
group_icons = ["person", "person-dress", "child"]
aside = {"loc": "upper left", "bbox_to_anchor": (1.02, 1), "frameon": False}

# 1. The first chart: one block is about 22 of the people aboard
fig, ax = waffle_chart(aboard, rows=10, columns=10, legend=aside, figsize=(6, 4))
fig.savefig(quickstart_image_folder + "first_chart.svg", bbox_inches="tight")
plt.close(fig)

# 2. Colours, a title, and the counts alongside the labels
fig, ax = waffle_chart(
    aboard,
    rows=10,
    columns=10,
    colors=class_colors,
    title={"label": "Who was aboard the Titanic: 2,201 people", "loc": "left"},
    legend=aside,
    show_values=True,
    figsize=(6.5, 4),
)
fig.savefig(quickstart_image_folder + "labelled.svg", bbox_inches="tight")
plt.close(fig)

# 3. rounding_rule="float". One block is 22 people, so rounding would shuffle whole
#    groups of them between categories. Partial blocks keep every share exact.
fig, ax = waffle_chart(
    aboard,
    rows=10,
    columns=10,
    colors=class_colors,
    rounding_rule="float",
    title={"label": "One block = 22 people, and nobody is rounded away", "loc": "left"},
    legend=aside,
    show_values="percentage",
    figsize=(6.5, 4),
)
fig.savefig(quickstart_image_folder + "fractional.svg", bbox_inches="tight")
plt.close(fig)

# 4. A continuous tiled grid, largest group first
fig, ax = waffle_chart(
    aboard,
    rows=10,
    columns=10,
    colors=class_colors,
    sort_values=True,
    rounding_rule="float",
    interval_ratio_x=0,
    interval_ratio_y=0,
    block_edge_color="white",
    block_edge_width=1.2,
    title={"label": "Who was aboard the Titanic: 2,201 people", "loc": "left"},
    legend=aside,
    show_values="percentage",
    figsize=(6.5, 4),
)
fig.savefig(quickstart_image_folder + "tiled.svg", bbox_inches="tight")
plt.close(fig)

# 5. Pictogram. The same 2,201 people cut a different way, one figure per 44 of them.
fig, ax = waffle_chart(
    by_group,
    rows=5,
    columns=10,
    colors=group_colors,
    icons=group_icons,
    font_size=22,
    icon_legend=True,
    background_color="#f4f2ee",
    title={"label": "One figure = 44 people aboard", "loc": "left"},
    legend=aside,
    show_values=True,
    figsize=(6.5, 2.8),
)
fig.savefig(quickstart_image_folder + "pictogram.svg", bbox_inches="tight")
plt.close(fig)

# 6. Subplots, and the reason the dataset is worth drawing at all. Only the last
#    panel carries the legend, and the others take a list so no labels are derived
#    from dict keys.
survival_plots = {}
for position, (group, total) in enumerate(aboard.items(), start=1):
    is_last = position == len(aboard)
    lived = saved[group]
    survival_plots[(1, 4, position)] = {
        "values": {"Survived": lived, "Lost": total - lived} if is_last else [lived, total - lived],
        "rows": 5,
        "columns": 10,
        "colors": ["#4a8f68", "#cfc9bf"],
        "rounding_rule": "float",
        "title": {"label": f"{group}\n{lived / total:.0%} survived", "loc": "left", "fontsize": 11},
        "interval_ratio_x": 0.15,
        "interval_ratio_y": 0.15,
        **({"legend": {"loc": "upper left", "bbox_to_anchor": (1.05, 1), "frameon": False}} if is_last else {}),
    }

fig = plt.figure(FigureClass=Waffle, figsize=(10, 2.4), plots=survival_plots)
fig.savefig(quickstart_image_folder + "survival.svg", bbox_inches="tight")
plt.close(fig)
