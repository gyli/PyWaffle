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
