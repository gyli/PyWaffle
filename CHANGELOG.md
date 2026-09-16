v1.2.0 (unreleased)

Fixes

* **Font Awesome icons now match the installed Font Awesome version.** The icon mapping was generated during installation, which never happens for a wheel install, so every release up to 1.1.1 shipped a Font Awesome 5.14 mapping while drawing from Font Awesome 6 fonts: 451 valid icon names raised `KeyError` and 83 names, including the digits `0`-`9`, `clock` and `hourglass-half`, silently rendered the wrong icon. The mapping is now built at runtime from the installed `fontawesomefree` package, and upgrading Font Awesome no longer requires reinstalling PyWaffle
* Fix icons and characters being sized wrongly on any figure whose DPI is not 96 - at 200 DPI they were about twice the intended size ([#33](https://github.com/gyli/PyWaffle/issues/33))
* Fix subplots sharing one legend, so that every subplot after the first rendered the first subplot's labels
* Fix the package being unbuildable by any PEP 517 frontend: `pip install .`, `pip install git+...` and `python -m build` all failed
* Support continuous colormaps in `cmap_name`. Previously anything other than a `ListedColormap` raised `AttributeError`, and the perceptual colormaps stored *as* `ListedColormap`s - `viridis`, `plasma`, `magma`, `inferno`, `cividis`, `turbo` - silently used the first few of their 256 entries, so every category came out the same shade. Qualitative palettes such as `Set2` are unchanged
* Replace the deprecated `set_tight_layout` with `set_layout_engine`, removing a warning on every figure
* Reject a negative or non-integer `rows` / `columns`, a non-positive `block_aspect_ratio`, a negative `interval_ratio_x` / `interval_ratio_y`, an unknown `plot_anchor`, and non-numeric `values` elements. `rows=-5` previously drew an empty chart with no error, and `plot_anchor='XX'` was accepted because matplotlib's `set_anchor` does not validate it either
* Refuse to draw a chart of more than `MAX_BLOCKS` (10,000,000) blocks. Values that were meant to be scaled previously turned into minutes of drawing rather than an error; the limit can be raised with `pywaffle.waffle.MAX_BLOCKS`
* Reject negative `values` and a `values` sum of zero up front, instead of silently drawing a wrong chart or raising `ZeroDivisionError`
* Reject values that come to zero blocks when only one of `rows` and `columns` is given. The other dimension is derived from the block count, so it came out zero, the block size came out negative, and the figure had negative axis extents. Reachable from ordinary values, not just zeros: `rounding_rule='floor'` maps anything below 1 to zero blocks
* Reject unknown `block_arranging_style`, which was previously accepted and silently drawn as `normal`
* Raise `ValueError` rather than `KeyError` or `AttributeError` for invalid `starting_location`, `rounding_rule` and `icon_style`, and accept `icon_style` lists in any case

New

* Add `rounding_rule="float"`, which draws partial blocks instead of rounding values ([#26](https://github.com/gyli/PyWaffle/issues/26)). A category that ends part way through a block fills only that fraction of it, and a block containing a boundary between two categories is split between their colors. The block count then depends only on the total of the values, so two datasets with the same total produce charts of the same size - which rounding did not guarantee
* Add `background_color`, which fills the space behind the blocks including the gaps between them, and `block_edge_color` / `block_edge_width`, which draw a border around each block ([#37](https://github.com/gyli/PyWaffle/issues/37))
* Add `show_values` and `value_format`, which append each category's value or its percentage of the total to its legend label. This is the f-string the documentation has always told people to write by hand: `labels=[f"{k} ({v}%)" for k, v in data.items()]`
* Add `sort_values` to order categories by value. Every per-category argument - `labels`, `colors`, `icons`, `characters` and `icon_style` - is reordered along with the values
* Take labels from a `pandas.Series` index, the same way they are already taken from a dict's keys
* Add a top-level `waffle_chart()` function with an explicit signature, so the parameters are visible to IDEs and `help()`, and a chart can be drawn straight into an existing axes with `ax=`. It is named `waffle_chart` rather than `waffle` so that it does not shadow the `pywaffle.waffle` module; `from pywaffle.functional import waffle` gives the shorter name. `plt.figure(FigureClass=Waffle, ...)` and `Waffle.make_waffle()` are unchanged and not deprecated

Other

* Add opt-in image-comparison tests (`pytest tests/test_images.py --mpl`), which catch rendering regressions that block-by-block assertions cannot
* `Waffle.make_waffle()` now raises `ValueError` when given `plots`, which it silently ignored. It draws into the single axis passed as `ax`, so `plots` never had any effect
* Add `pywaffle.__version__`
* Ship `py.typed`, so the existing type hints are visible to type checkers
* Require Python 3.9+, and move packaging to PEP 621
* Add continuous integration: test matrix, lint, and a build that installs the sdist and the wheel into clean environments

---

v1.1.1 (2024-06-16)

* Support matplotlib>=3.9.0 by fixing get_cmap calling

---

v1.1.0 (2022-06-07)

* Replace embedded Font Awesome files with dependent Python package `fintawesomefree`
* Generate Font Awesome mapping file automatically during installation, so it can allow manual Font Awesome version upgrade

---

v1.0.1 (2022-06-03)

* Add support to plot chart on existed axis
* Remove deprecated parameter `icon_set`
* Refactor `Waffle` class
* Remove unnecessary variable copying
* Remove `Waffle._pa` as it only contains arguments of last subplot

---

v0.6.4 (2021-12-21)

* Fix wrong license in icon mapping file
* Fix extra block caused by two or more consecutive zeros in values

---

v0.6.3 (2021-07-27)

* Fix extra block with default rounding method

---

v0.6.2 (2021-07-23)

* Fix wrong block number when block_arranging_style is `new-line`

---

v0.6.0 (2020-07-18)

* Add parameter `block_arranging_style`
* Fix parameter `vertical` not being used when it's set in `plots`
* Fix wrong direction when `starting_location` is `SE` or `NE`

---

v0.4.1 (2019-10-14)

* Make either one of `rows` and `columsn` optional
* Remove deprecated parameter `plot_direction`
* Add online demo

---

v0.3.2 (2019-10-11)

* Add parameter `characters`, `font_file` and `font_size` for plotting with characters.
* Add parameter `tight`
* Add more tests

---

v0.2.5 (2019-10-06)

* Rename parameter `block_aspect` to `block_aspect_ratio`
* Deprecate `icon_set`, use `icon_style` instead. `icon_style` accepts font style for each icon
* Deprecate `plot_direction`, use `starting_location` instead
* Finished documents with more examples. See [https://pywaffle.readthedocs.io/](https://pywaffle.readthedocs.io/)

---

v0.2.0 (2018-11-25)

* Update Font Awesome to 5.5.0

---

v0.0.7 (2017-11-22)

* First public version
