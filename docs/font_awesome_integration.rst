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

Using a system Font Awesome
---------------------------

PyWaffle does not need the Python package specifically -- it needs the fonts. Set
:code:`PYWAFFLE_FONTAWESOME_DIR` to a directory of Font Awesome ``.otf`` files and they are used
instead::

   $ export PYWAFFLE_FONTAWESOME_DIR=/usr/share/fonts/fontawesome

If neither the environment variable nor the Python package provides the fonts, the usual system
font directories are searched, so a distribution's font package is often enough on its own:

* Fedora, ``fontawesome-6-free-fonts`` and ``fontawesome-6-brands-fonts``
* Arch, ``otf-font-awesome`` in :code:`/usr/share/fonts/OTF`
* Debian and Ubuntu, ``fonts-font-awesome``

Distribution packages ship the fonts without Font Awesome's ``icons.json``, so in that case the
icon names are recovered from the fonts themselves -- Font Awesome stores each icon's name as its
glyph name, so the character map gives every name back. Two consequences worth knowing:

* **Aliases are unavailable.** They exist only in ``icons.json``, so ``circle-half-stroke`` works
  while its alias ``adjust`` does not.
* Some icons resolve to a different code point, because Font Awesome maps both a private-use code
  point and the matching real Unicode one to the same glyph. The chart is unchanged; only the
  character behind it differs.

Everything else is identical, including which icons exist.

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
