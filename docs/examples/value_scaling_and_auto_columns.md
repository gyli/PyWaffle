# Value Scaling and Auto-columns

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
