.. PyWaffle documentation master file, created by
   sphinx-quickstart on Wed Nov 22 16:25:01 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyWaffle Documentation
======================

PyWaffle is an open source, MIT-licensed Python package for plotting waffle charts — also known as
square pie charts, and, when drawn with icons, pictogram charts.

.. image:: https://raw.githubusercontent.com/gyli/PyWaffle/master/examples/quickstart/tiled.svg?sanitize=true
   :alt: World electricity generation in 2025, drawn as a waffle chart
   :align: center

A waffle chart is a grid of blocks where one block stands for a fixed quantity, so a proportion is
something the reader can count rather than estimate.

.. code:: python

   from pywaffle import waffle_chart

   fig, ax = waffle_chart({"Coal": 33.0, "Gas": 21.8, "Hydro": 14.0}, rows=10, columns=10)

PyWaffle is also a `Figure constructor
<https://matplotlib.org/gallery/subplots_axes_and_figures/custom_figure_class.html>`_ class *Waffle*,
which can be passed to matplotlib.pyplot.figure to generate a matplotlib Figure object. Both forms
are fully supported — see the :doc:`quickstart`.

Visit PyWaffle on `Github
<https://github.com/gyli/PyWaffle>`_ and `PyPI
<https://pypi.org/project/pywaffle/>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   examples
   font_awesome_integration
   class
