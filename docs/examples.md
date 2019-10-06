# Examples

Several examples are shown below, which would go through every parameter. Please check out [Constructor Class](class.html) for the detail of parameter.


## Basic

```python
import matplotlib.pyplot as plt
from pywaffle import Waffle
```

Plot a 5-row, 10-column chart with a list of values. The three values here, 48, 46 and 6 are represented by 24, 23 and 3 blocks.
```python
plt.figure(
    FigureClass=Waffle, 
    rows=5,
    columns=10, 
    values=[48, 46, 6]
)
```

<img class="img_middle" alt="With list values" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/basic_list_values.svg?sanitize=true">

Parameter `values` also accept dict data. The key of the dict would be used as labels and legends.

```python
plt.figure(
    FigureClass=Waffle, 
    rows=5,
    columns=10, 
    values={'Cat1': 20, 'Cat2': 12, 'Cat3': 8}, 
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)}
)
```

<img class="img_middle" alt="With dict values" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/basic_dict_values.svg?sanitize=true">

## Value Scaling and Auto-columns

A more common case is, the chart size does not equal to the total number of values. Then the values might be scaled to fit the chart size.

Change argument `rounding_rule` to set a preferred rounding rule when scaling.

> **_NOTE:_** When `rounding_rule` is `ceil` or `nearest`, the total number of scaled value might be greater than chart size, while it would not be shown in the plot. Thus some block numbers might change if the order of values are changed.

With `rounding_rule`=`floor`, the values are scaled to 24, 23, 1 as block numbers.

```python
plt.figure(
    FigureClass=Waffle, 
    rows=5,
    columns=10, 
    values=[48, 46, 3],
    rounding_rule='floor'
)
```

<img class="img_middle" alt="Rounding rule" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/value_scaling_and_auto_columns_rounding_rule.svg?sanitize=true">

To avoid scaling values as block numbers, argument `columns` can be ignored and only passing `rows`. Then the absolute number of `values` would be used as block number directly and `columns` would be calculated automatically.

```python
plt.figure(
    FigureClass=Waffle, 
    rows=10,
    values=[48, 46, 3]
)
```

<img class="img_middle" alt="Ignore columns" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/value_scaling_and_auto_columns_ignore_columns.svg?sanitize=true">

## Title, Label and Legend

Parameter `title` accepts parameters of [matplotlib.axes.Axes.set_title](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_title.html) in a dict.

Parameter `labels` accepts labels in a list. If it is not specified, key of `values` would be used as labels.

Parameter `legend` accepts parameters of [matplotlib.pyplot.legend](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html) in a dict.

```python
data = {'Cat1': 48, 'Cat2': 46, 'Cat3': 3}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    title={
        'label': 'Example plot', 
        'loc': 'left', 
        'fontdict': {
            'fontsize': 20
        }
    },
    labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
    legend={
        'loc': 'lower left', 
        'bbox_to_anchor': (0, -0.4), 
        'ncol': len(data), 
        'framealpha': 0, 
        'fontsize': 12
    }
)
```

<img class="img_middle" alt="Title, Label and Legend" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/title_label_ledend.svg?sanitize=true">

> **_NOTE:_** Labels could also be specified in parameter `legend` as an item instead.

## Block Color and Background Color

Parameter `colors` accepts colors in a list or tuple. The length must be the same as values.

```python
fig = plt.figure(
    FigureClass=Waffle, 
    rows=5,
    columns=10,
    values=[48, 46, 3], 
    colors=["#983D3D", "#232066", "#DCB732"]
)
fig.set_facecolor('#EEEEEE')
```

<img class="img_middle" alt="Block Color and Background Color" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_color_and_background_color.svg?sanitize=true">

## Icons

PyWaffle supports [Font Awesome icons](https://fontawesome.com/). Blocks could be icons instead of squares.

```python
fig = plt.figure(
    FigureClass=Waffle, 
    rows=5, 
    values=[48, 46, 3], 
    colors=("#232066", "#983D3D", "#DCB732"),
    icons='child', 
    icon_size=12, 
)
```
    
<img class="img_middle" alt="Icons" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/icons.svg?sanitize=true">

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
