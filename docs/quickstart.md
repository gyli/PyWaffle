# Quickstart

A waffle chart is a grid of blocks where **one block stands for a fixed quantity**. That is the whole
idea: instead of asking someone to judge the angle of a pie slice, you ask them to count squares.

Everything below uses one dataset, the people aboard the Titanic, carried from the first chart to the
last so that each step adds a single idea.

```{note}
Figures from the British Board of Trade inquiry of 1912: 2,201 aboard, 710 saved, 1,491 lost.
Tabulated at [Sinking of the
Titanic](https://en.wikipedia.org/wiki/Sinking_of_the_Titanic#Casualties_and_survivors).
```

## Install

```shell
pip install pywaffle
```

## Your first chart

Pass a dict and say how big the grid is. The keys become the labels.

```python
import matplotlib.pyplot as plt
from pywaffle import waffle_chart

aboard = {"First class": 325, "Second class": 285, "Third class": 706, "Crew": 885}

aside = {"loc": "upper left", "bbox_to_anchor": (1.02, 1), "frameon": False}

fig, ax = waffle_chart(aboard, rows=10, columns=10, legend=aside, figsize=(6, 4))
```

<img class="img_middle" alt="Who was aboard the Titanic, by class" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/first_chart.svg?sanitize=true">

2,201 people in a grid of 100 blocks, so **one block is about 22 people**. `waffle_chart()` returns
the matplotlib `(figure, axes)` pair, so everything you already know about matplotlib still applies.

`legend` is passed straight through to
[`Axes.legend`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html). Putting
it outside the axes keeps it off the blocks.

## Colours, a title, and the numbers

```python
class_colors = ["#c9a227", "#5f8a8b", "#b5653f", "#3d4f5d"]

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
```

<img class="img_middle" alt="The same chart with colours, a title and counts in the legend" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/labelled.svg?sanitize=true">

`show_values=True` appends each category's number to its legend label. `show_values="percentage"`
shows its share of the total instead, and `value_format` controls how either is written.

## Nobody rounded away

A block is a whole thing, so a share that falls part way through one normally has to be rounded. Here
a block is 22 people, so rounding moves whole groups of them from one class to another.
`rounding_rule="float"` stops that. A category that ends mid-block fills only that fraction of it, and
a block holding a boundary is split between two colours.

```python
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
```

<img class="img_middle" alt="Fractional blocks, where a category ending mid-block fills only part of it" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/fractional.svg?sanitize=true">

A useful side effect: the number of blocks now depends only on the total, so two datasets with the
same total always produce a chart of the same size.

## A continuous grid

Close the gaps and give each block an edge, and the chart reads as one tiled surface rather than
floating squares. `sort_values=True` puts the largest group first and carries each category's colour
along with it.

```python
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
```

<img class="img_middle" alt="A continuous tiled grid with white block edges" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/tiled.svg?sanitize=true">

## Icons, for a pictogram chart

Swap the rectangles for [Font Awesome](https://fontawesome.com/icons?d=gallery&m=free) icons and the
chart becomes a pictogram, where one figure stands for a number of people. This is the same 2,201
people, cut by group instead of by class.

```python
by_group = {"Men": 1667, "Women": 425, "Children": 109}

fig, ax = waffle_chart(
    by_group,
    rows=5,
    columns=10,
    colors=["#3d4f5d", "#c9a227", "#b5653f"],
    icons=["person", "person-dress", "child"],
    font_size=22,
    icon_legend=True,
    background_color="#f4f2ee",
    title={"label": "One figure = 44 people aboard", "loc": "left"},
    legend=aside,
    show_values=True,
    figsize=(6.5, 2.8),
)
```

<img class="img_middle" alt="The people aboard drawn as a pictogram of men, women and children" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/pictogram.svg?sanitize=true">

`icon_legend=True` uses the icons in the legend instead of colour swatches. Icons are drawn as text
and so have no block edge to colour, which is what `background_color` is for. It works behind
rectangle blocks too.

## Several charts in one figure

`plots` takes a dict of subplot position to arguments. Anything you set at the figure level is the
default for every subplot, and each subplot can override it.

```python
saved = {"First class": 202, "Second class": 118, "Third class": 178, "Crew": 212}

survival_plots = {}
for position, (group, total) in enumerate(aboard.items(), start=1):
    is_last = position == len(aboard)
    lived = saved[group]
    survival_plots[(1, 4, position)] = {
        # Only the last panel gets labels, so only it draws a legend
        "values": {"Survived": lived, "Lost": total - lived} if is_last else [lived, total - lived],
        "rows": 5,
        "columns": 10,
        "colors": ["#4a8f68", "#cfc9bf"],
        "rounding_rule": "float",
        "title": {"label": f"{group}\n{lived / total:.0%} survived", "loc": "left", "fontsize": 11},
        "interval_ratio_x": 0.15,
        "interval_ratio_y": 0.15,
    }
survival_plots[(1, 4, 4)]["legend"] = {"loc": "upper left", "bbox_to_anchor": (1.05, 1), "frameon": False}

fig = plt.figure(FigureClass=Waffle, figsize=(10, 2.4), plots=survival_plots)
```

<img class="img_middle" alt="Survival rate by class, as four small waffle charts" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/survival.svg?sanitize=true">

## Into a layout you already have

Pass `ax` to draw into an axes you have already made, instead of building a new figure:

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 3))

waffle_chart(aboard, rows=5, columns=10, colors=class_colors, ax=axes[0])
waffle_chart(by_group, rows=5, columns=10, colors=["#3d4f5d", "#c9a227", "#b5653f"],
             icons=["person", "person-dress", "child"], font_size=14, ax=axes[1])
```

No figure-level arguments such as `figsize` or `dpi` are accepted in this form. Set those on the
figure that owns the axes.

## The other two ways to call it

These build the same chart. Use whichever reads better in your code.

```python
from pywaffle import Waffle

# The matplotlib-native form, used throughout the Examples pages
fig = plt.figure(FigureClass=Waffle, rows=10, columns=10, values=aboard)

# Straight onto an existing axes
fig, ax = plt.subplots()
Waffle.make_waffle(ax=ax, rows=10, columns=10, values=aboard)
```

## Where next

- {doc}`examples` — every parameter, by topic
- {doc}`class` — the full parameter list
- {doc}`font_awesome_integration` — icon names, and how to change Font Awesome version
