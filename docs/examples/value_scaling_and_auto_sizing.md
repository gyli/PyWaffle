# Value Scaling and Auto-sizing

## Value Scaling

It is a common case that the chart size does not equal to the total number of values. Then the values have to be scaled to fit the chart size.

Change argument `rounding_rule` to set a preferred rounding rule when scaling. It accepts `floor` or `ceil` or `nearest`.

> **_NOTE:_** When `rounding_rule` is `ceil` or `nearest`, sum of scaled values might be greater than chart size. If so, the blocks of last category would not be shown completely in the chart. Therefore, although `nearest` is the default rounding rule, `floor` is actually the most consistent rule as it avoids the block overflowing. 

In the following example, values are scaled to 24, 23, 1 as block numbers with `rounding_rule`=`floor`.

```python
plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    rounding_rule='floor'
)
```

<img class="img_middle" alt="Rounding rule" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/value_scaling_and_auto_sizing_rounding_rule.svg?sanitize=true">

---

## Auto-sizing

If you would like to avoid values scaling, pass an integer to either one of `rows` or `columns` parameter only. Then the absolute number of `values` would be used as block number directly and the other parameter would be calculated automatically.

In the following example, we set `rows=5`, `values=[48, 46, 3]` and leave `columns` empty. Then the block numbers would be the same to values. Since the sum of values is 97, the column number has to be 20 to fit all blocks.

```python
plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[48, 46, 3]
)
```

<img class="img_middle" alt="Ignore columns" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/value_scaling_and_auto_sizing_ignore_columns.svg?sanitize=true">
