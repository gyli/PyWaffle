# Block Shape, Spacing, Location, Direction and Arranging Style

PyWaffle provides several parameters to control how and where to plot blocks.

## Block Shape

Parameter `block_aspect_ratio` controls the shape of blocks by change the ratio of block's width to block's height. By default it is 1, so that the blocks are squares.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    block_aspect_ratio=1.618
)
```

<img class="img_middle" alt="Change Block Shape" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_shape.svg?sanitize=true">

---

## Block Spacing

Parameter `interval_ratio_x` and `interval_ratio_y` control the horizontal and vertical distance between blocks. `interval_ratio_x` is the ratio of horizontal distance between blocks to block's width and `interval_ratio_y` is the ratio of vertical distance between blocks to block's height.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    interval_ratio_x=1,
    interval_ratio_y=0.5
)
```

<img class="img_middle" alt="Change Block Distance" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_distance.svg?sanitize=true">

---

## Where to Start First Block

Use parameter `starting_location` to set the location of starting block. It accepts locations in string like `NW`, `SW`, `NE` and `SE` representing four corners. By default, it is `SW`, meaning PyWaffle starts drawing blocks from lower-left corner.

Here is an example that start plotting from lower-right corner (`SE`).

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    starting_location='SE'
)
```

<img class="img_middle" alt="Change Starting Location" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_location.svg?sanitize=true">

---

## Plotting Direction

By default, PyWaffle draws blocks column by column, thus categories are plotted horizontally. To make it vertical, set parameter `vertical` to `True`.

In the following example, it draws blocks from lower-left corner to lower-right corner row by row up to the top.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[30, 16, 4],
    vertical=True
)
```

<img class="img_middle" alt="Change Direction" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_direction.svg?sanitize=true">

---

## Where to Start Each Category

Use parameter `block_arranging_style` to set how to arrange blocks for each category. By default it is `'normal'`, which draws block of new category from where last category ends.

When it is `snake`, it draws with snake pattern, starting a new line from an opposite direction every time. This style is useful if you would like to keep blocks of each category together.

In the below example, since the default starting location is lower-left and default direction is not vertical, it draws blocks from lower-left to top-left for the first line, and then from the top block of second column down to the bottom one of this column, and then go on with snake-like pattern.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[12, 22, 20, 4],
    block_arranging_style='snake'
)
```

<img class="img_middle" alt="Change Starting Location" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/snake_pattern.svg?sanitize=true">

When it is `new-line`, it forces every category starting from a new line. Note that it only works when only `columns` is passed and `vertical`=`True`, or `rows` is passes and `vertical`=`False`. It will be ignored if both of `columns` and `rows` are passed. 

```python
fig = plt.figure(
    FigureClass=Waffle,
    columns=10,
    values=[30, 16, 4],
    block_arranging_style='new-line',
    vertical=True
)
```

<img class="img_middle" alt="Change Starting Location" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/new_line_pattern.svg?sanitize=true">
