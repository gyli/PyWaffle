# Plot on Existed Axis

Sometimes you might have figure and axis created already, and you are looking for a way to plot waffle chart on top of 
it, without creating a new figure. In this case, you may use `Waffle.make_waffle()` function. It accepts axis `ax` and all other arguments available in
`Waffle`. It is a classmethod, and you should call it without creating a new `Waffle` instance.

```python
fig = plt.figure()
ax = fig.add_subplot(111)

# Modify existed axis
ax.set_title("Axis Title")
ax.set_aspect(aspect="equal")

Waffle.make_waffle(
    ax=ax,  # pass axis to make_waffle
    rows=5, 
    columns=10, 
    values=[30, 16, 4], 
    title={"label": "Waffle Title", "loc": "left"}
)
```

<img class="img_middle" alt="With list values" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/plot_on_existed_axis.svg?sanitize=true">
