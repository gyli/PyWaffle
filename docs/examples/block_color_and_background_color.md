# Block Color and Background Color

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

<img class="img_middle" alt="Block Color and Background Color" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_color_and_background_color.svg?sanitize=true">

[Colormap](https://matplotlib.org/gallery/color/colormap_reference.html) could also be applied to waffle chart, which sets colors automatically. Sequential colormaps do not work with PyWaffle and only Qualitative colormaps are supported, including `Pastel1`, `Pastel2`, `Paired`, `Accent`, `Dark2`, `Set1`, `Set2`, `Set3`, `tab10`, `tab20`, `tab20b`, `tab20c`.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    cmap_name="tab10"
)
```

<img class="img_middle" alt="Block Color with custom cmap_name" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_color_and_background_color_custom_cmap_name.svg?sanitize=true">
