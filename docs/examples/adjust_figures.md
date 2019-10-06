# Adjust Figures

## Background Color
Parameter `colors` accepts colors in a list or tuple. The length must be the same as `values`.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    colors=["#983D3D", "#232066", "#DCB732"]
)
fig.set_facecolor('#EEEEEE')
```

<img class="img_middle" alt="Adjust Figures - Change Background Color" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/adjust_figure_change_background.svg?sanitize=true">

---

## Plot Location

Use parameter `plot_anchor` to change the location of plot in the figure.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    plot_anchor='S'
)
fig.set_facecolor('#EEEEEE')
```

<img class="img_middle" alt="Adjust Figures - Change Plot Location" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/adjust_figure_location.svg?sanitize=true">
