# Add Other Elements

Although PyWaffle provides parameters like `title` and `legend` to add elements, it is only for plotting waffle charts after all. To add other elements and make a fancy plot, you can update the figure directly or use the methods provided by Figure class. 

In the following example, we use `text()` method to add a custom watermark to the figure.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4]
)
fig.text(
    x=0.5,
    y=0.5,
    s="Sample",
    ha="center",
    va="center",
    rotation=30,
    fontsize=40,
    color='gray',
    alpha=0.3,
    bbox={
        'boxstyle': 'square', 
        'lw': 3, 
        'ec': 'gray', 
        'fc': (0.9, 0.9, 0.9, 0.5), 
        'alpha': 0.3
    }
)
```

<img class="img_middle" alt="Add Watermark" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/add_other_elements.svg?sanitize=true">

You may also use method like `add_artist` to add custom objects, which is not a method of PyWaffle, but its parent class `matplotlib.figure.Figure`. See [matplotlib.figure.Figure](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_artist) for all available methods.
