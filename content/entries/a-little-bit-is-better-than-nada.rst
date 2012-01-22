title: A Little Bit is Better Than Nada
type: entry
category: entries
datetime: 2012-01-22 12:00:00
---

It is a running joke in the `X.Org`_ community that X12 development will
commence as soon as all of the X11 bugs in the `FreeDesktop.org bug tracker`_
have been closed. When I first heard this, my reaction was, of course,
"Challenge accepted!" But where to start?

There were about 10,000 bugs open on the tracker at that point, a few years
ago. We're definitely improving; there are about 9180 bugs open (at the time
of writing) which could be considered relevant to any kind of desktop
development. Many of those don't belong to anything in X11, but assuming they
did...

Pretend that all of the card-carrying members of X.Org closed 92 bugs. That
would be 1% per person. We could be done with X11! So, during XDC 2011, I
pulled out my netbook, and started closing bugs. I picked, as my targets,
things that nobody would miss, like Xprint.

I closed some Xprint-related bugs, before simply shuttering everything in the
Xprint product. I also picked up a couple of stray bugs. Finally, with
maintainer permission, I closed everything still assigned to xf86-video-nv.

The results:

 * 24 Xprint-related bugs
 * 37 bugs in Product: xprint
 * 42 bugs in Component: driver/nv
 * 37 bugs in Component: driver/nVidia (open)
 * #9455, #28657, #29832, #30129

A total of 144 bugs. We can do this, guys!

.. _`X.Org`: http://www.x.org/
.. _`FreeDesktop.org bug tracker`: http://bugs.freedesktop.org/
