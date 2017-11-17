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

Basic example:

.. code:: python

    import matplotlib.pyplot as plt
    from pywaffle import Waffle

    fig = plt.figure(FigureClass=Waffle, rows=6, columns=10, values=[30, 20, 10])
    plt.show()

.. image:: README_images/basic.png
    :width: 640
    :alt: Pywaffle basic example


License
-------

PyWaffle uses the MIT license, see ``LICENSE`` file for the details.
