# Examples

Several examples are shown below, which would go through every argument. Please check out [Constructor Class](class.html) for the detail of argument.


## Basic

```python
import matplotlib.pyplot as plt
from pywaffle import Waffle
```

Plot a 5*10 chart. The three values here, 48, 46 and 6 are represented by 24, 23 and 3 blocks.
```python
plt.figure(
    FigureClass=Waffle, 
    rows=5,
    columns=10, 
    values=[48, 46, 6]
)
```

![basic](https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/readme/basic-1.svg)

A more common case is, the chart size does not fit the total number of blocks. Then the values would be scaled to fit the chart size.

Change argument `rounding_rule` to set a preferred rounding rule.

> **_NOTE:_** When `rounding_rule` is `CEIL` or `NEAREST`, the total number of scaled value might be greater than chart size, while it would not be shown in the plot. Thus some block numbers might change if the order of values are changed.

With `rounding_rule`=`FLOOR`, the values are shrinked to 24, 23, 1 as block number.

```python
plt.figure(
    FigureClass=Waffle, 
    rows=5,
    columns=10, 
    values=[48, 46, 3],
    rounding_rule='FLOOR'
)
```

![basic](https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/readme/basic-2.svg)

To avoid scaling values as block numbers, argument `columns` can be ignored and only passing `rows`. Then `values` would be used as block number directly and `columns` would be calculated automatically.

```python
plt.figure(
    FigureClass=Waffle, 
    rows=5,
    values=[48, 46, 3]
)
```

![basic](https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/readme/basic-3.svg)

## 2. Values in dict & Auto-columns

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

If parameter `columns` is empty, PyWaffle uses absolute number in `values` as block number.

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
fig.gca().set_facecolor('#EEEEEE')
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
    icons='child', icon_size=12, 
    icon_legend=True
)
```
    
![Use Font Awesome icons](examples/readme/fontawesome.svg)

PyWaffle supports [Font Awesome](http://fontawesome.io/) icons in the chart.

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
    rows=5,
    colors=("#2196f3", "#ff5252", "#999999"),  # Default argument values for subplots
    figsize=(9, 5)  # figsize is a parameter of plt.figure
)
```
    
![Multiple plots](examples/readme/multiple_plots.svg)

In this chart, 1 block = 30000 votes.

<sub>Data source [https://en.wikipedia.org/wiki/United_States_presidential_election,_2016](https://en.wikipedia.org/wiki/United_States_presidential_election,_2016).</sub>
