Infinite Space

I am releasing a small library that I have been working on in my spare time.
Specifically, time spent in hotel rooms. <a
href="http://github.com/MostAwesomeDude/continued">Continued</a> is a library
that implements basic conversion and arithmetic for <a
href="http://en.wikipedia.org/wiki/Continued_fraction">continued
fractions</a>. This initial release contains a bevy of ways to create
continued fractions, and the four basic arithmetic operators.

<code class="pycon">
>>> import continued
>>> continued.Pi()
Continued(3, 7, 15, 1, 292, 1, 1, 1, 2, ...)
>>> continued.E()
Continued(2, 1, 2, 1, 1, 4, 1, 1, 6, ...)
>>> continued.E() * continued.Pi()
Continued(8, 1, 1, 5, 1, 3, 1, 4, 12, ...)
>>> continued.E() + continued.Pi()
Continued(5, 1, 6, 7, 3, 21, 2, 1, 2, ...)
</code>

Have fun with this. There's at least one outstanding bug, and undoubtedly more
will surface as people try it out. The package is available on <a
href="http://pypi.python.org/">PyPI</a> as <a
href="http://pypi.python.org/pypi/continued">"continued"</a>.
