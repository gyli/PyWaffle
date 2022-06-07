Font Awesome Integration
========================

PyWaffle installs `Font Awesome
<https://fontawesome.com/>`_ free version automatically as a package dependency.
The package it is trying to install is the latest version of `fontawesomefree
<https://pypi.org/project/fontawesomefree/>`_.

If you would like to upgrade :code:`fontawesomefree` and use the newer version with PyWaffle, you can simply upgrade :code:`fontawesomefree` and reinstall :code:`pywaffle`. In commands, that is:

::

   $ pip install --upgrade fontawesomefree
   $ pip install pywaffle

By running the above commands, PyWaffle will generate a new icon mapping for the newer version :code:`fontawesomefree` under the package directory, and takes care of everything. You will be free to start using new icons!

For how to use Font Awesome with PyWaffle, please see `Plot with Characters or Icons
<examples/plot_with_characters_or_icons.md>`_.