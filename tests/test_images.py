#!/usr/bin/python
# -*-coding: utf-8 -*-
"""Image-comparison tests.

PyWaffle's job is to put coloured rectangles in the right places, and the assertions elsewhere in
this suite check that numerically - block counts, coordinates, colours. What they cannot catch is a
change that is correct block by block and still wrong as a picture: a layout engine change, a
matplotlib default moving underneath us, a legend drifting over the chart.

These tests render a small set of charts and compare them against committed baseline images. They
are opt-in and are skipped unless pytest-mpl is installed and --mpl is passed, because pytest-mpl
runs the test body without comparing anything when the flag is absent, and a test that reports
success while checking nothing is worse than no test at all.

The baselines are generated on macOS and compared on Linux in CI. That works because matplotlib
ships its own fonts, so text renders identically on both.

Regenerate the baselines after an intended visual change:

    pytest tests/test_images.py --mpl-generate-path=tests/baseline

and inspect the diff before committing it.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from pywaffle.waffle import Waffle

# Without the plugin there is nothing to compare against, so skip the module rather than
# registering markers that do nothing
pytest.importorskip("pytest_mpl", reason="image comparison requires pytest-mpl")


@pytest.fixture(autouse=True)
def _require_mpl_flag(request):
    """Skip unless --mpl was passed.

    pytest-mpl runs the test body but performs no comparison when --mpl is absent, so these would
    otherwise report as passing while checking nothing - worse than not running at all.
    """
    if not request.config.getoption("--mpl", default=False):
        pytest.skip("image comparison requires --mpl")


# A fixed style, so a change to matplotlib's defaults cannot move the baselines underneath us
STYLE = "classic"
TOLERANCE = 5


def waffle_figure(**kwargs):
    kwargs.setdefault("figsize", (5, 3))
    kwargs.setdefault("dpi", 100)
    return plt.figure(FigureClass=Waffle, **kwargs)


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_basic():
    return waffle_figure(rows=5, columns=10, values=[48, 46, 6])


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_auto_sized_from_rows():
    return waffle_figure(rows=5, values=[30, 16, 4])


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_title_and_legend():
    data = {"Democratic": 48, "Republican": 46, "Libertarian": 6}
    return waffle_figure(
        rows=5,
        columns=10,
        values=data,
        colors=("#983D3D", "#232066", "#DCB732"),
        title={"label": "Vote Percentage", "loc": "left"},
        legend={"loc": "lower left", "bbox_to_anchor": (0, -0.4), "ncol": 3, "framealpha": 0},
    )


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_block_shape_and_spacing():
    return waffle_figure(
        rows=5,
        columns=10,
        values=[30, 16, 4],
        block_aspect_ratio=1.5,
        interval_ratio_x=0.5,
        interval_ratio_y=0.1,
    )


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_snake_arrangement():
    return waffle_figure(rows=5, values=[12, 22, 20, 4], block_arranging_style="snake")


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_vertical_and_starting_location():
    return waffle_figure(rows=5, columns=10, values=[30, 16, 4], vertical=True, starting_location="NE")


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_characters():
    return waffle_figure(rows=5, columns=10, values=[30, 16, 4], characters="*", font_size=20)


@pytest.mark.mpl_image_compare(style=STYLE, tolerance=TOLERANCE, savefig_kwargs={"bbox_inches": "tight"})
def test_subplots():
    return plt.figure(
        FigureClass=Waffle,
        figsize=(5, 4),
        dpi=100,
        rows=5,
        plots={
            211: {"values": [10, 20, 30], "labels": ["A", "B", "C"]},
            212: {"values": [30, 20, 10], "labels": ["D", "E", "F"]},
        },
    )
