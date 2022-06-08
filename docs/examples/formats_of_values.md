# Basic Examples and Formats of Values

This is a simple example to plot a 5-row, 10-column waffle chart. The three values are plotted as blocks directly, 
and the blocks number matches the numbers in `values`, because the sum of `values` equals to total block number (`rows * columns`).

Parameter `values` accept numbers in multiple format, including list, dict, and pandas.DataFrame. 

```python
import matplotlib.pyplot as plt
from pywaffle import Waffle
```

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,  # Either rows or columns could be omitted
    values=[30, 16, 4]  # Pass a list of integers to values
)
fig.savefig("plot.png", bbox_inches="tight")
```

<img class="img_middle" alt="With list values" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/basic_list_values.svg?sanitize=true">

> **_NOTE:_** One of the parameter `rows` and `columns` is redundant in this case, since both of the chart size and value sum are 50. So, either one of `rows` and `columns` could be omitted, and it can still be calculated through value sum automatically. See [Auto-sizing](value_scaling_and_auto_sizing.md) for more details. 

---

When a dictionary is passed to `values`, the key will be used as labels and shown in legends.

```python
plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values={'Cat1': 30, 'Cat2': 16, 'Cat3': 4},
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)}
)
```

<img class="img_middle" alt="With dict values" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/basic_dict_values.svg?sanitize=true">

---

However, unlike values in a dictionary that can generate labels and legend automatically, when the `values` is a DataFrame, `Waffle` does not use the row index of the DataFrame as label by default. So you have to pass the index to parameter `labels` manually, if you would like to use column index as label.

```python
import pandas as pd

data = [30, 16, 4]
df = pd.DataFrame(data, columns=['Value'], index=['Cat1', 'Cat2', 'Cat3'])


plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=df['Value'],
    labels=list(df.index),  # Legend would not be created without this line
    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)}
)
```
