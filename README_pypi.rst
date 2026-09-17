PyWaffle
========

.. image:: https://badge.fury.io/py/pywaffle.svg
 :target: https://pypi.org/project/pywaffle/

.. image:: https://readthedocs.org/projects/pywaffle/badge/?version=latest&style=flat
 :target: https://readthedocs.org/projects/pywaffle/badge/?version=latest&style=flat

.. image:: https://img.shields.io/badge/run-Online%20Demo-blue
 :target: https://mybinder.org/v2/gh/gyli/PyWaffle/master?filepath=demo.ipynb

Introduction
------------

PyWaffle is an open source, MIT-licensed Python package for plotting waffle charts.

It provides a `Figure constructor class <https://matplotlib.org/gallery/subplots_axes_and_figures/custom_figure_class.html>`_ ``Waffle``, which could be passed to `matplotlib.pyplot.figure <https://matplotlib.org/api/_as_gen/matplotlib.pyplot.figure.html>`_ and generates a matplotlib Figure object.

Installation
------------

.. code:: bash

    pip install pywaffle

Quickstart
----------

.. code:: python

    from pywaffle import waffle_chart

    fig, ax = waffle_chart([48, 46, 6], rows=5, columns=10, figsize=(5, 3))

``waffle_chart()`` returns the matplotlib ``(figure, axes)`` pair, and takes ``ax=`` to draw into a
layout you already have. The figure-class form below builds the same chart and is equally supported:

.. code:: python

    import matplotlib.pyplot as plt
    from pywaffle import Waffle

    fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 6])

Demo
----

`Online Demo <https://mybinder.org/v2/gh/gyli/PyWaffle/master?filepath=demo.ipynb>`_

Documentation
-------------

`https://pywaffle.readthedocs.io/ <https://pywaffle.readthedocs.io/>`_

License
-------

* PyWaffle is under MIT license, see `LICENSE` file for the details.
* The Font Awesome font is licensed under the SIL OFL 1.1: `http://scripts.sil.org/OFL <http://scripts.sil.org/OFL>`_
