# Block Directions

PyWaffle provides several parameters to control how and where to plot blocks.

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

[Colormap](https://matplotlib.org/gallery/color/colormap_reference.html) could also be applied to waffle chart through parameter `cmap_name`, which sets colors automatically. 
