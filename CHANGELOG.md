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
