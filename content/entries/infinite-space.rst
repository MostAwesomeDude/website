title: Infinite Space
type: entry
category: entries
datetime: 2010-09-24 01:59:24
---

I am releasing a small library that I have been working on in my spare time.
Specifically, time spent in hotel rooms.  Continued_ is a library that
implements basic conversion and arithmetic for `continued fractions`_. This
initial release contains a bevy of ways to create continued fractions, and the
four basic arithmetic operators.

.. sourcecode:: pycon

    >>> import continued
    >>> continued.Pi()
    Continued(3, 7, 15, 1, 292, 1, 1, 1, 2, ...)
    >>> continued.E()
    Continued(2, 1, 2, 1, 1, 4, 1, 1, 6, ...)
    >>> continued.E() * continued.Pi()
    Continued(8, 1, 1, 5, 1, 3, 1, 4, 12, ...)
    >>> continued.E() + continued.Pi()
    Continued(5, 1, 6, 7, 3, 21, 2, 1, 2, ...)

Have fun with this. There's at least one outstanding bug, and undoubtedly more
will surface as people try it out. The package is available on PyPI_ as
`"continued"`_.

.. _Continued: http://github.com/MostAwesomeDude/continued
.. _continued fractions: http://en.wikipedia.org/wiki/Continued_fraction
.. _PyPI: http://pypi.python.org/
.. _"continued": http://pypi.python.org/pypi/continued
