title: Poison Was the Cure
type: entry
category: entries
datetime: 2011-10-03 10:16:59
---

glyph_ and I met for the first time a few weeks ago, and ever since, he's been
asking me to do things. Write code, review patches, write blog posts, that
kind of thing. Being the lazy person I am, I'm not really up-front or speedy
about doing things outside of my habitual box. Thankfully, I got inspired by a
troll.

Everybody's read Ted Dziuba's `fantastic anti-Node troll`_, right? It's good
food for thought, even if it is a little bit belligerent. I wanted to
demonstrate that Twisted_ doesn't have the same problems as Node. I also
wanted to write a small application for Heroku_, because I participated in
their Python beta and figured out how to run Twisted applications on their
platform.

So, I wrote a tiny application that does a few things. First, it runs on
Heroku. It includes the Procfile magic for running on Heroku correctly, and
only depends on Twisted. Second, it calculates Fibonacci numbers. The idiom
that I chose to implement involves not caching the numbers, and instead using
threads to do background work. I was going to do something highly idiomatic
and Twisted-like, such as setting a timer and coming back to do the work
later, but I wanted to show off a feature of Twisted which is completely
missing from Node: The ability to write threaded code without leaving your
language.

That's right, **Node.js does not have the ability to host multiple threads in
JavaScript**. (Correct me if I'm wrong, but after a half-hour of research and
an `assertion I made on Hacker News`_ which went unchallenged, I'm pretty sure
that this is the case.) Why? I don't know. Possibly because Node's tied to
V8, which is very shiny but certainly not as cool as the dominant Python
implementations, like CPython_ or PyPy_. Now, make no mistake, many Pythons
have GILs or fine-grained locks, which can slow down threaded code, but Node
can't even attempt to thread off its CPU-bound long-running computations, and
I think that's an important ability to have. And as a well-known
anti-threading advocate, when *I* admit that threads have their uses, I hope
people notice.

I also got very annoyed at everybody who felt that they were demonstrating the
benefits of Node by writing equivalent servers in Python using the standard
library. Python's built-in servers suck. They straight-up suck. Would you
deploy a web server written in pure JavaScript with only the standard library
shipped with all JavaScript implementations? Probably not! Just like one needs
Node to write those servers, Python developers use Twisted to provide that
functionality. Otherwise, you're deliberately crippling your examples in order
to skew impressions of Python. I'm going to shame you here, because you should
know better. You should know about Twisted, if for no other reason than that
it is listed on the front page of Node.js_'s homepage as one of the
inspirations for Node. No, really, go check. I'll wait here.

The actual Heroku side of things is kind of boring. Heroku's Python support is
fantastic. Use the cedar stack when you create your app with ``heroku
apps:create --stack cedar`` and put a line into your Procfile which passes the
``$PORT`` shell variable into your app somehow. If you're deploying stock
Twisted Web, something like ``bin/python ./twistd -n web --port=$PORT`` is a
good starter. You can, of course, easily deploy WSGI apps on top of this using
``--wsgi``. You *must not daemonize* on Heroku. That's really about it; it's a
very straightforward platform which is easy to use and I'm very impressed by
their work.

I have an application running on Heroku right now. The link is currently
`right here <http://radiant-stone-8394.herokuapp.com/>`_ although it might be
taken down in a few months when I need to experiment more. I'm a free
customer, you see, and I'm not willing to pay a monthly fee just to prove a
point about people on the Internets. Anyway, the application does nothing
except check how many threads are running on the system, calculate a Fibonacci
number, and tell you how long the request took. It can do this for many
concurrent users; you might notice, if there are many active requests, that
the page will stop loading halfway through as your request to calculate a
Fibonacci number sits in line in a threadpool. Your actual browser connection
won't be dropped, though.

The code is a demonstration of Heroku's cedar stack and a few fancier things
in Twisted Web, like the new templating system added in Twisted 11.0. You can
find it on Github; the repo is called "cancer_" for obvious reasons.

Oh, and as a closer: Some people have complained heavily about the idiom that
was demonstrated at the end of Ted's rant. The reason that he posted that is
that JavaScript programmers, unlike Python programmers, never really got in
the habit of not using names which haven't been declared or defined. The idiom
in Python looks like this:

.. sourcecode:: python

    if my_var is not None:
        ...

We don't check to see if ``my_var in locals()`` or anything stupid like that,
because ``my_var`` should be easy to track and the line where it was defined
should be obvious. If it's not, you're writing bad code.

.. _glyph: http://glyph.twistedmatrix.com/
.. _fantastic anti-Node troll: http://teddziuba.com/2011/10/node-js-is-cancer.html
.. _Twisted: http://twistedmatrix.com/
.. _Heroku: http://heroku.com/
.. _assertion I made on Hacker News: http://news.ycombinator.com/item?id=3063157
.. _CPython: http://python.org/
.. _PyPy: http://pypy.org/
.. _Node.js: http://nodejs.org/
.. _cancer: http://github.com/MostAwesomeDude/cancer
