============
Installation
============

The last stable release is available on PyPI and can be installed with ``pip``::

   $ pip install pywaffle

.. rubric:: Requirements

* Python 3.9+
* Matplotlib

.. rubric:: Drawing with icons

Icons come from `Font Awesome <https://fontawesome.com/>`_, which is an **optional** dependency.
Install it alongside PyWaffle if you want pictogram charts::

   $ pip install "pywaffle[icons]"

Everything except the ``icons`` parameter works without it, including ``characters``, which uses
an ordinary font. Passing ``icons`` without the extra raises ``ImportError`` with the command to
run.
