# Basic Examples

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
