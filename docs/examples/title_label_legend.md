# Title, Label and Legend

Parameter `title` accepts parameters of [matplotlib.pyplot.title](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.title.html) in a dict.

Parameter `labels` accepts string labels in a list. If it is not specified, key of `values` would be used as labels.

Parameter `legend` accepts parameters of [matplotlib.pyplot.legend](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html) in a dict.

> **_NOTE:_** Labels could also be specified in parameter `legend` under key `labels` instead.

```python
data = {'Cat1': 30, 'Cat2': 16, 'Cat3': 4}
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=data,
    title={
        'label': 'Example plot',
        'loc': 'left',
        'fontdict': {
            'fontsize': 20
        }
    },
    labels=[f"{k} ({int(v / sum(data.values()) * 100)}%)" for k, v in data.items()],
    legend={
        # 'labels': [f"{k} ({v}%)" for k, v in data.items()],  # lebels could also be under legend instead
        'loc': 'lower left',
        'bbox_to_anchor': (0, -0.4),
        'ncol': len(data),
        'framealpha': 0,
        'fontsize': 12
    }
)
```

<img class="img_middle" alt="Title, Label and Legend" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/title_label_ledend.svg?sanitize=true">

---

## Showing Values in the Legend

Use `show_values` to put each category's number next to its name, instead of building the label
strings yourself.

```python
data = {'Cat1': 10, 'Cat2': 7, 'Cat3': 9}

plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    show_values=True,  # Cat1 (10)
)
```

`show_values='percentage'` shows each category's share of the total instead, and `value_format`
controls how the number is written.

```python
plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=data,
    show_values='percentage',       # Cat1 (38.5%)
    value_format='{:.2f}%',         # Cat1 (38.46%)
)
```

The default format is `'{:g}'` for values and `'{:.1f}%'` for percentages.

---

## Sorting Categories

`sort_values=True` orders the categories largest first, and `'asc'` smallest first. Every
per-category argument — `labels`, `colors`, `icons`, `characters` and `icon_style` — is reordered
along with the values, so a category keeps its own colour and icon.

```python
plt.figure(
    FigureClass=Waffle,
    rows=5,
    values={'A': 5, 'B': 20, 'C': 10},
    colors=['red', 'green', 'blue'],
    sort_values=True,  # B, C, A - and green, blue, red
)
```
