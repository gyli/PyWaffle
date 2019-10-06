# PyWaffle

PyPI page: [https://pypi.org/project/pywaffle/](https://pypi.org/project/pywaffle/)

Documentation: [http://pywaffle.readthedocs.io/](http://pywaffle.readthedocs.io/)

## Introduction

PyWaffle is a Python package to plot waffle chart.

It provides a [Figure constructor class](https://matplotlib.org/gallery/subplots_axes_and_figures/custom_figure_class.html) `Waffle`, which could be passed to [matplotlib.pyplot.figure](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.figure.html) and generate a matplotlib Figure object.

## Installation

```python
pip install pywaffle
```

## Requirements

* Python 3
* Matplotlib

## Examples

### 1. Basic Example

```python
import matplotlib.pyplot as plt
from pywaffle import Waffle
```

```python
# The values are rounded to 10 * 5 blocks
fig = plt.figure(
    FigureClass=Waffle, 
    rows=5, 
    columns=10, 
    values=[48, 46, 3]
)
plt.show()
```

![basic](examples/readme/basic.svg)

### 2. Values in dict & Auto-columns

```python
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle, 
    rows=5, 
    values=data, 
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)}
)
plt.show()
```

![Use values in dictionary; use absolute value as block number, without defining columns](examples/readme/absolute_block_numbers.svg)

If argument `columns` is empty, PyWaffle uses absolute number in `values` as block number.

If `values` is a dict, its keys are used as labels.

### 3. Title, Legend, Colors, Background Color, Block Color and Direction

```python
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle, 
    rows=5, 
    values=data, 
    colors=("#983D3D", "#232066", "#DCB732"),
    title={'label': 'Vote Percentage in 2016 US Presidential Election', 'loc': 'left'},
    labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
    legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.4), 'ncol': len(data), 'framealpha': 0},
    plot_direction='NW'
)
fig.set_facecolor('#EEEEEE')
plt.show()
```

![Add title, legend and background color; customize the block color](examples/readme/title_and_legend.svg)

It is now clear to see that there are 3% votes to other parties/candidates.

### 4. Icons

```python
data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
fig = plt.figure(
    FigureClass=Waffle, 
    rows=5, 
    values=data, 
    colors=("#232066", "#983D3D", "#DCB732"),
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)},
    icons='child', 
    icon_size=12, 
    icon_legend=True
)
```
    
![Use Font Awesome icons](examples/readme/fontawesome.svg)

PyWaffle supports [Font Awesome](https://fontawesome.com/) icons in the chart.

### 5. Multiple Plots

```python
import pandas as pd
data = pd.DataFrame(
    {
        'labels': ['Hillary Clinton', 'Donald Trump', 'Others'],
        'Virginia': [1981473, 1769443, 233715],
        'Maryland': [1677928, 943169, 160349],
        'West Virginia': [188794, 489371, 36258],
    },
).set_index('labels')

# A glance of the data:
#                  Maryland  Virginia  West Virginia
# labels                                            
# Hillary Clinton   1677928   1981473         188794
# Donald Trump       943169   1769443         489371
# Others             160349    233715          36258


fig = plt.figure(
    FigureClass=Waffle,
    plots={
        '311': {
            'values': data['Virginia'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['Virginia'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1), 'fontsize': 8},
            'title': {'label': '2016 Virginia Presidential Election Results', 'loc': 'left'}
        },
        '312': {
            'values': data['Maryland'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['Maryland'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.2, 1), 'fontsize': 8},
            'title': {'label': '2016 Maryland Presidential Election Results', 'loc': 'left'}
        },
        '313': {
            'values': data['West Virginia'] / 30000,
            'labels': ["{0} ({1})".format(n, v) for n, v in data['West Virginia'].items()],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.3, 1), 'fontsize': 8},
            'title': {'label': '2016 West Virginia Presidential Election Results', 'loc': 'left'}
        },
    },
    rows=5,  # shared parameter among subplots
    colors=("#2196f3", "#ff5252", "#999999"),  # shared parameter among subplots
    figsize=(9, 5)  # figsize is a parameter of plt.figure
)
```
    
![Multiple plots](examples/readme/multiple_plots.svg)

In this chart, 1 block = 30000 votes.

<sub>Data source [https://en.wikipedia.org/wiki/United_States_presidential_election,_2016](https://en.wikipedia.org/wiki/United_States_presidential_election,_2016).</sub>


## What's New
Verion 0.2.5:

* Rename `block_aspect` to `block_aspect_ratio`
* Deprecate `icon_set`, use `icon_style` instead. `icon_style` accepts font style for each icon
* Deprecate `plot_direction`, use `starting_location` instead
* Finished documents with more examples. See [https://pywaffle.readthedocs.io/](https://pywaffle.readthedocs.io/)

## License

* PyWaffle is under MIT license, see `LICENSE` file for the details.
* The Font Awesome font is licensed under the SIL OFL 1.1: http://scripts.sil.org/OFL
