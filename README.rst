PyWaffle
========

PyPI page: https://pypi.python.org/pypi/pywaffle

Documentation: Working on it

Introduction
------------

PyWaffle is a Python package to make waffle chart, bases on `Matplotlib <https://matplotlib.org/>`__.

Please note that this package is under heavy development currently. Do NOT use it until it reaches the first stable version.

Installation
------------

.. code:: bash

    pip install pywaffle

Examples
--------

1. Basic example:

.. code:: python

    import matplotlib.pyplot as plt
    from pywaffle import Waffle

    # The percentage is rounded to 10 * 5 blocks
    fig = plt.figure(FigureClass=Waffle, rows=5, columns=10, values=[48, 46, 3])
    plt.show()

.. raw:: html

    <img src="README_images/basic.png", width="50%" height="50%">

2. Use values in dictionary; use absolute value as block number, without defining columns:

.. code:: python

    data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
    fig = plt.figure(FigureClass=Waffle, rows=5, values=data, legend_conf={'loc': (0, -0.3)})
    plt.show()

.. raw:: html

    <img src="README_images/absolute_block_numbers.png", width="50%" height="50%">

3. Add title, legend and background color; customize the block color:

.. code:: python

    data = {'Democratic': 48, 'Republican': 46, 'Libertarian': 3}
    fig = plt.figure(FigureClass=Waffle, rows=5, values=data,
                     title_conf={'label': 'Vote Percentage in 2016 US Presidential Election', 'loc': 'left'},
                     colors=("#983D3D", "#232066", "#DCB732"),
                     labels=["{0} ({1}%)".format(k, v) for k, v in data.items()],
                     legend_conf={'loc': (0, -0.3), 'facecolor': '#EEEEEE', 'fontsize': 10})
    fig.gca().set_facecolor('#EEEEEE')
    fig.set_facecolor('#EEEEEE')
    plt.show()

.. raw:: html

    <img src="README_images/title_and_legend.png", width="50%" height="50%">

Data source `https://en.wikipedia.org/wiki/United_States_presidential_election,_2016 <https://en.wikipedia.org/wiki/United_States_presidential_election,_2016>`__.

License
-------

PyWaffle uses the MIT license, see ``LICENSE`` file for the details.
