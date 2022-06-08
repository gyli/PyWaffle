Font Awesome Integration
========================

PyWaffle installs `Font Awesome
<https://fontawesome.com/>`_ free version automatically as a package dependency.
The package it is trying to install is the latest version of `fontawesomefree
<https://pypi.org/project/fontawesomefree/>`_.

If you would like to upgrade or downgrade :code:`fontawesomefree`, and use the specific version within PyWaffle, you can upgrade :code:`fontawesomefree` and then reinstall :code:`pywaffle`. In commands, that is:

::


   # Either upgrade to the latest, or specify a version number
   pip install --upgrade fontawesomefree
   # OR
   pip install fontawesomefree==6.1.1

   # Then reinstall pywaffle
   pip install --force-reinstall --no-deps pywaffle

Option :code:`--force-reinstal` ensures icon mapping file in the package would be regenerated, and option :code:`--no-deps` avoid package :code:`fontawesomefree` being upgraded to unexpected version.

To validate the upgrade, you may check the version number at the first line of the icon mapping file. The file path is :code:`<PYTHON_LIB>/pywaffle/fontawesome_mapping.py`

For how to use Font Awesome with PyWaffle, please visit `Plot with Characters or Icons
<examples/plot_with_characters_or_icons.html#icons>`_.