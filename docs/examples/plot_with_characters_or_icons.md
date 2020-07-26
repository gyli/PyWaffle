# Plot with Characters or Icons

## Characters

Blocks could be Unicode characters instead of rectangles by passing the desired character to `characters`. 

Categories could have different character for each category, by passing a list or tuple of characters to parameter `characters` . The length must be the same as `values`.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    colors=["#4C8CB5", "#B7CBD7", "#C0C0C0"],
    characters='⬤',
    font_size=24
)
```

<img class="img_middle" alt="Icons" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/characters.svg?sanitize=true">

To specify the font, pass the absolute path to a .ttf or .otf file to parameter `font_file`.

---

## Icons

PyWaffle supports [Font Awesome icons](https://fontawesome.com/).

When using icons, the parameters for setting block size would be ignored, including `interval_ratio_x`, `interval_ratio_y` and `block_aspect_ratio`. Instead, use `icon_size` to set the size of icons. For availale sizes, visit [FontProperties.set_size](https://matplotlib.org/api/font_manager_api.html#matplotlib.font_manager.FontProperties.set_size).

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    colors=["#232066", "#983D3D", "#DCB732"],
    icons='star',
    font_size=24
)
```
    
<img class="img_middle" alt="Icons" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/icons.svg?sanitize=true">

Each categories could have a different icon, by passing a list or tuple of icon names to parameter `icons`. The length must be the same as `values`.

In Font Awesome Icons, there are different icon sets in different styles, including Solid, Regular and Brands. It can be specified through parameter `icon_style`. By default it searches icon from `solid` style.

With `icon_legend`=`True`, the symbol in legend would be the icon. Otherwise, it would be a color bar.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    colors=["#FFA500", "#4384FF", "#C0C0C0"],
    icons=['sun', 'cloud-showers-heavy', 'snowflake'],
    font_size=20,
    icon_style='solid',
    icon_legend=True,
    legend={
        'labels': ['Sun', 'Shower', 'Snow'], 
        'loc': 'upper left', 
        'bbox_to_anchor': (1, 1)
    }
)
```

<img class="img_middle" alt="Icons per category" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/icons_different_per_category.svg?sanitize=true">

Font Awesome Icons locates icons by style and icon name. Different styles contain different sets of icons. Thus icon_style might not be the same for all icons. In this case, `icon_style` could be a list or a tuple of styles. 

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    colors=["#FFA500", "#4384FF", "#C0C0C0"],
    icons=['sun', 'cloud-showers-heavy', 'font-awesome-flag'],
    icon_size=20,
    icon_style=['regular', 'solid', 'brands'],
    icon_legend=False,
    legend={
        'labels': ['Sun', 'Shower', 'Flag'], 
        'loc': 'upper left', 
        'bbox_to_anchor': (1, 1)
    }
)
```

<img class="img_middle" alt="Icons with different styles" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/icons_different_style.svg?sanitize=true">
