# Block Colors

Parameter `colors` accepts colors in a list or tuple. The length must be same to `values`, and the acceptable color format includes case-insensitive hex RGB or RGBA, RGB or RGBA tuple, single character notation, case-insensitive X11/CSS4 color name, and more, as long as Matplotlib can recognize. See Matplotlib [Colors](https://matplotlib.org/stable/tutorials/colors/colors.html#specifying-colors) for the full list.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[30, 16, 4],
    colors=["#232066", "#983D3D", "#DCB732"]
)
```

<img class="img_middle" alt="Block Colors" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_colors.svg?sanitize=true">

Another method to change block colors is passing [Colormap](https://matplotlib.org/stable/gallery/color/colormap_reference.html) to parameter `cmap_name`, which sets colors in batch. 

> **_NOTE:_** Sequential colormaps does not work with PyWaffle. Only Qualitative colormaps are supported, including `Pastel1`, `Pastel2`, `Paired`, `Accent`, `Dark2`, `Set1`, `Set2`, `Set3`, `tab10`, `tab20`, `tab20b`, `tab20c`. See the list and color examples in [Colormaps in Matplotlib](https://matplotlib.org/stable/tutorials/colors/colormaps.html#qualitative).

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[30, 16, 4],
    cmap_name="tab10"
)
```

<img class="img_middle" alt="Block Colors with custom cmap_name" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_colors_custom_cmap_name.svg?sanitize=true">
