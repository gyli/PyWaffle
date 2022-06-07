# Subplots

Sometimes we would like to show multiple waffle charts in one figure. 
This is supported through adding subplots. It also helps avoiding duplicated legends, titles and other components.

Let's say we have sample data as shown below:

```python
import pandas as pd
data = pd.DataFrame(
    {
        'labels': ['Car', 'Truck', 'Motorcycle'],
        'Factory A': [32384, 13354, 5245],
        'Factory B': [22147, 6678, 2156],
        'Factory C': [8932, 3879, 896],
    },
).set_index('labels')

# A glance of the data:
#             Factory A  Factory B  Factory C
# labels
# Car             27384      22147       8932
# Truck            7354       6678       3879
# Motorcycle       3245       2156       1196
```

To convert the Vehicle Production data above into reasonable block numbers, we can simply pass values like `data['Factory A'] / 1000`, and PyWaffle will handle the [rounding](value_scaling_and_auto_sizing.md#value-scaling). 
Note that parameter `values` also accepts column data in `pandas.Series`. 
However, unlike values in dict, pandas.Series value does not support auto labeling yet.

To plot multiple subplots in one figure, merge the parameters for each plot to parameter `plots` as dict values. 
The keys are integers describing the position of the subplot. 
It accepts tuple, int and string. 
If position is tuple, the format should be like `(nrows, ncols, index)`; 
if it is int or string, it should be a 3-digit integer like `312`, standing for nrows, ncols, and index in order. 
Note that all integers must be less than 10 for the later form to work. 
See arguments of [matplotlib.pyplot.subplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot.html) for more detail.

> **_NOTE:_** Parameters which are passed outside of `plots` would be applied to all subplots, if they are not specified in `plots`.
Otherwise, settings in `plots` have higher priority.

```python
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

```

<img class="img_middle" alt="Multiple subplots" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/readme/multiple_plots.svg?sanitize=true">
