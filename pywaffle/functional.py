#!/usr/bin/python
# -*-coding: utf-8 -*-
"""
A plain function wrapping the Waffle figure class.

``plt.figure(FigureClass=Waffle, ...)`` is the matplotlib-native way to build a waffle chart and
remains fully supported, but it hides every real parameter behind ``**kwargs``: it does not
autocomplete, ``help()`` shows nothing useful, and it always builds a whole Figure even when the
caller wants one panel of an existing layout. This module spells the parameters out.
"""

from typing import Dict, Iterable, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .waffle import Waffle

__all__ = ["waffle"]


def waffle(
    values: Union[List, Tuple, Dict, Iterable],
    rows: Optional[int] = None,
    columns: Optional[int] = None,
    *,
    ax: Optional[Axes] = None,
    colors: Optional[Union[List[str], Tuple[str, ...]]] = None,
    labels: Optional[Union[List[str], Tuple[str, ...]]] = None,
    legend: Optional[Dict] = None,
    characters: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
    font_file: Optional[str] = None,
    font_size: Optional[Union[int, str]] = None,
    icons: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
    icon_style: Union[str, List[str], Tuple[str, ...]] = "solid",
    icon_legend: bool = False,
    interval_ratio_x: float = 0.2,
    interval_ratio_y: float = 0.2,
    block_aspect_ratio: float = 1,
    cmap_name: str = "Set2",
    title: Optional[Dict] = None,
    plot_anchor: str = "W",
    vertical: bool = False,
    starting_location: str = "SW",
    rounding_rule: str = "nearest",
    tight: Union[bool, Dict, None] = True,
    block_arranging_style: str = "normal",
    **kwargs,
):
    """
    Plot a waffle chart.

    Run it with code like::

        fig, ax = waffle([48, 46, 6], rows=5)

    or draw into an axes you already have::

        fig, axes = plt.subplots(1, 2)
        waffle({"Yes": 70, "No": 30}, rows=5, ax=axes[0])

    This is a wrapper around the :class:`~pywaffle.waffle.Waffle` figure class. Every parameter
    behaves exactly as documented there; see :class:`~pywaffle.waffle.Waffle` for the full
    reference. The two matplotlib-native forms remain supported and are not deprecated::

        plt.figure(FigureClass=Waffle, rows=5, values=[48, 46, 6])
        Waffle.make_waffle(ax=ax, rows=5, values=[48, 46, 6])

    :param values: Numerical value of each category. If it is a dict, the keys are used as labels.
    :type values: list|dict|tuple|pandas.Series

    :param rows: The number of lines of the waffle chart.
    :type rows: int, optional

    :param columns: The number of columns of the waffle chart.

        | At least one of rows and columns is required.
    :type columns: int, optional

    :param ax: Draw into this axes instead of creating a new figure.

        | When given, the axes' figure is returned rather than a new one, and no figure-level
          arguments (such as ``figsize`` or ``dpi``) are accepted.
    :type ax: matplotlib.axes.Axes, optional

    :param \*\*kwargs: Additional arguments passed to
        :func:`matplotlib.pyplot.figure`, such as ``figsize``, ``dpi`` or ``facecolor``.
        Only accepted when ``ax`` is not given.

    :return: ``(figure, axes)``
    :rtype: tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
    """
    waffle_args = {
        "values": values,
        "rows": rows,
        "columns": columns,
        "colors": colors,
        "labels": labels,
        "legend": legend if legend is not None else {},
        "characters": characters,
        "font_file": font_file,
        "font_size": font_size,
        "icons": icons,
        "icon_style": icon_style,
        "icon_legend": icon_legend,
        "interval_ratio_x": interval_ratio_x,
        "interval_ratio_y": interval_ratio_y,
        "block_aspect_ratio": block_aspect_ratio,
        "cmap_name": cmap_name,
        "title": title,
        "plot_anchor": plot_anchor,
        "vertical": vertical,
        "starting_location": starting_location,
        "rounding_rule": rounding_rule,
        "tight": tight,
        "block_arranging_style": block_arranging_style,
    }

    if ax is not None:
        if kwargs:
            raise TypeError(
                f"Figure arguments are not accepted when drawing into an existing axes: "
                f"{', '.join(sorted(kwargs))}. Set them on the figure that owns the axes instead."
            )
        Waffle.make_waffle(ax=ax, **waffle_args)
        return ax.figure, ax

    fig: Figure = plt.figure(FigureClass=Waffle, **waffle_args, **kwargs)
    return fig, fig.axes[0]
