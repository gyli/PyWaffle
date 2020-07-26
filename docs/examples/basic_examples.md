# Basic Examples

This is a simplest example to plot a 5-row, 10-column waffle chart. The three values are plotted as blocks directly.

> **_NOTE:_** One of the parameter rows and columns is redundant in this case, since both of the chart size and value sum are 50. So, either one of rows and columns could be omitted, and it can still be calculated through value sum automatically. See [Auto-sizing](value_scaling_and_auto_sizing.md#Auto-sizing) for more details. 

```python
import matplotlib.pyplot as plt
from pywaffle import Waffle
```

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,  # Either rows or columns could be omitted
    values=[30, 16, 4]
)
fig.show()
```

<img class="img_middle" alt="With list values" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/basic_list_values.svg?sanitize=true">

Parameter `values` also accepts data in dict. The key of the dict would be used as labels and shown in legends.

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
