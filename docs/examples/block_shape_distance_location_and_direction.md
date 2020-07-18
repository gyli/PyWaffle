# Block Size, Distance, Location and Direction

PyWaffle provides several parameters to control how and where to plot blocks.

## Adjust Block Shape

Parameter `block_aspect_ratio` controls the shape of blocks by change the ratio of block's width to block's height. By default it is 1, so that the blocks are squares.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    block_aspect_ratio=1.618,
)
```

<img class="img_middle" alt="Change Block Shape" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_shape.svg?sanitize=true">

---

## Adjust Block Distance

Parameter `interval_ratio_x` and `interval_ratio_y` control the horizontal and vertical distance between blocks. `interval_ratio_x` is the ratio of horizontal distance between blocks to block's width and `interval_ratio_y` is the ratio of vertical distance between blocks to block's height.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    interval_ratio_x=1,
    interval_ratio_y=0.5
)
```

<img class="img_middle" alt="Change Block Distance" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_distance.svg?sanitize=true">

---

## Where to start my first block

Use parameter `starting_location` to set the location of starting block. It accepts locations in string like `NW`, `SW`, `NE` and `SE` representing four corners. By default, it is `SW`, meaning PyWaffle starts drawing blocks from bottom left corner.

Here is an example that start plotting from bottom left corner.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    starting_location='SE'
)
```

---

## Where to start each category

Use parameter `contiguous_blocks` to set whether starting each category from a new column or new row. By default it is True, so when drawing a new category it will start from where last category ends.

Parameter `contiguous_blocks` only works when only one of `columns` and `rows` is set. It will be ignored if both of `columns` and `rows` are set. 

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    values=[48, 46, 3],
    contiguous_blocks=False
)
```

<img class="img_middle" alt="Change Starting Location" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/contiguous_blocks.svg?sanitize=true">

---

## The direction of plotting next block

By default, PyWaffle draws plots column by column. As a result, categories are plotted horizontally. To make the it vertical, just set parameter `vertical` to `True`.

```python
fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=10,
    values=[48, 46, 3],
    vertical=True
)
```

<img class="img_middle" alt="Change Direction" src="https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/docs/block_direction.svg?sanitize=true">
