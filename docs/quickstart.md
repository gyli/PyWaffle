# Quickstart

A waffle chart is a grid of blocks where **one block stands for a fixed quantity**. That is the whole
idea: instead of asking someone to judge the angle of a pie slice, you ask them to count squares.

Everything below is one dataset — how the world generated its electricity in 2025 — carried from the
first chart to the last, so each step adds a single idea.

```{note}
Data: [Ember (2026) via Our World in Data](https://ourworldindata.org/grapher/share-elec-by-source),
"Share of electricity production by source", 2025. Both CC BY 4.0. Oil, bioenergy and other
renewables are grouped here as "Other".
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

electricity = {
    "Coal": 33.0,
    "Gas": 21.8,
    "Hydro": 14.0,
    "Nuclear": 8.8,
    "Solar": 8.7,
    "Wind": 8.5,
    "Other": 5.2,
}

aside = {"loc": "upper left", "bbox_to_anchor": (1.02, 1), "frameon": False}

fig, ax = waffle_chart(electricity, rows=10, columns=10, legend=aside, figsize=(6, 4))
```

<img class="img_middle" alt="A first waffle chart of world electricity generation" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/first_chart.svg?sanitize=true">

The values sum to 100 and the grid holds 100 blocks, so **one block is one percent of the world's
electricity**. `waffle_chart()` returns the matplotlib `(figure, axes)` pair, so everything you
already know about matplotlib still applies.

`legend` is passed straight through to
[`Axes.legend`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html); putting
it outside the axes keeps it off the blocks.

## Colours, a title, and the numbers

```python
energy_colors = ["#44413d", "#c4703a", "#2e6fa7", "#7a4b9e", "#f2b705", "#3fa796", "#b9b6b0"]

fig, ax = waffle_chart(
    electricity,
    rows=10,
    columns=10,
    colors=energy_colors,
    title={"label": "How the world made its electricity in 2025", "loc": "left"},
    legend=aside,
    show_values=True,
    value_format="{:g}%",
    figsize=(6.5, 4),
)
```

<img class="img_middle" alt="The same chart with colours, a title and values in the legend" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/labelled.svg?sanitize=true">

`show_values=True` appends each category's number to its legend label, and `value_format` controls how
it is written. Use `show_values="percentage"` to show each category's share of the total instead of
the value itself.

## Nothing rounded away

A block is a whole thing, so a share that falls part way through one normally has to be rounded.
`rounding_rule="float"` stops that: a category that ends mid-block fills only that fraction of it, and
a block holding a boundary is split between two colours.

It shows best on a smaller grid, where one block is worth more:

```python
fig, ax = waffle_chart(
    electricity,
    rows=5,
    columns=10,
    colors=energy_colors,
    rounding_rule="float",
    title={"label": "One block = 2%, and nothing is rounded away", "loc": "left"},
    legend=aside,
    show_values=True,
    value_format="{:g}%",
    figsize=(6.5, 2.8),
)
```

<img class="img_middle" alt="Fractional blocks, where a category ending mid-block fills only part of it" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/fractional.svg?sanitize=true">

Fifty blocks for seven shares that are not multiples of 2% — every boundary lands inside a block, and
every one of them is drawn where it actually falls. A useful side effect: the number of blocks now
depends only on the total, so two datasets with the same total always produce the same size of chart.

## A continuous grid

Close the gaps and give each block an edge, and the chart reads as one tiled surface rather than
floating squares. `sort_values=True` puts the largest share first, carrying each category's colour
along with it.

```python
fig, ax = waffle_chart(
    electricity,
    rows=10,
    columns=10,
    colors=energy_colors,
    sort_values=True,
    rounding_rule="float",
    interval_ratio_x=0,
    interval_ratio_y=0,
    block_edge_color="white",
    block_edge_width=1.2,
    title={"label": "World electricity generation, 2025", "loc": "left"},
    legend=aside,
    show_values=True,
    value_format="{:g}%",
    figsize=(6.5, 4),
)
```

<img class="img_middle" alt="A continuous tiled grid with white block edges" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/tiled.svg?sanitize=true">

## Icons, for a pictogram chart

Swap the rectangles for [Font Awesome](https://fontawesome.com/icons?d=gallery&m=free) icons and the
same data becomes a pictogram chart.

```python
energy_icons = ["fire", "gas-pump", "water", "atom", "solar-panel", "fan", "plug"]

fig, ax = waffle_chart(
    electricity,
    rows=5,
    columns=10,
    colors=energy_colors,
    icons=energy_icons,
    font_size=20,
    icon_legend=True,
    background_color="#f4f2ee",
    title={"label": "World electricity generation, 2025", "loc": "left"},
    legend=aside,
    figsize=(6.5, 2.8),
)
```

<img class="img_middle" alt="The same data drawn as a pictogram chart with energy icons" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/pictogram.svg?sanitize=true">

`icon_legend=True` uses the icons in the legend instead of colour swatches. Icons are drawn as text
and so have no block edge to colour — `background_color` is how you give the grid a panel to sit on,
and it works for rectangle blocks too.

## Into a layout you already have

Pass `ax` to draw into an axes you have already made, instead of building a new figure:

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 3))

waffle_chart(electricity, rows=5, columns=10, colors=energy_colors, ax=axes[0])
waffle_chart(electricity, rows=5, columns=10, colors=energy_colors, icons=energy_icons,
             font_size=14, ax=axes[1])
```

No figure-level arguments such as `figsize` or `dpi` are accepted in this form — set those on the
figure that owns the axes.

## The other two ways to call it

These build exactly the same chart. Use whichever reads better in your code.

```python
from pywaffle import Waffle

# The matplotlib-native form, used throughout the Examples pages
fig = plt.figure(FigureClass=Waffle, rows=10, columns=10, values=electricity)

# Straight onto an existing axes
fig, ax = plt.subplots()
Waffle.make_waffle(ax=ax, rows=10, columns=10, values=electricity)
```

## Where next

- {doc}`examples` — every parameter, by topic
- {doc}`class` — the full parameter list
- {doc}`font_awesome_integration` — icon names, and how to change Font Awesome version
