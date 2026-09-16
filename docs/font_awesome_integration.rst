Font Awesome Integration
========================

Icons come from the free version of `Font Awesome
<https://fontawesome.com/>`_, packaged for Python as `fontawesomefree
<https://pypi.org/project/fontawesomefree/>`_.

It is an **optional** dependency, so install it alongside PyWaffle when you want icons::

   $ pip install "pywaffle[icons]"

Nothing else needs it. Rectangle blocks, and the ``characters`` parameter, work without it, and
asking for ``icons`` when it is absent raises ``ImportError`` naming the command to run rather than
a bare ``ModuleNotFoundError``.

Upgrading or downgrading Font Awesome
-------------------------------------

Install the version of :code:`fontawesomefree` you want. PyWaffle picks it up on the next run;
there is nothing else to do and no need to reinstall PyWaffle.

::

   # Either upgrade to the latest, or specify a version number
   pip install --upgrade fontawesomefree
   # OR
   pip install fontawesomefree==6.1.1

PyWaffle builds the icon name to character mapping from the installed :code:`fontawesomefree`
package, the first time a chart uses icons in a given session. The names you can use and the
glyphs you get therefore always come from the same Font Awesome version.

To check which version is in use:

::

   pip show fontawesomefree

.. note::

   Before PyWaffle 1.2.0 the mapping was a file generated during installation, which required
   :code:`pip install --force-reinstall --no-deps pywaffle` after every Font Awesome change. That
   step regenerated nothing for wheel installs, so PyWaffle up to 1.1.1 shipped a Font Awesome
   5.14 mapping regardless of the font version installed. If you use icons, upgrade to 1.2.0 or
   later: on older versions several hundred valid icon names raise :code:`KeyError`, and a number
   of others silently draw the wrong icon.

For how to use Font Awesome with PyWaffle, please visit `Plot with Characters or Icons
<examples/plot_with_characters_or_icons.html#icons>`_.
