title: Lessons
type: entry
category: entries
datetime: 2012-09-21 15:09:00
---

I have a problem. It's not an unusual problem, and I wish to tackle it
precisely because of its ubiquity. The problem is, roughly, this: I have a
large chunk of code which does some blocking work. I wish to augment this code
so that it can be used with `Twisted`_, and I wish to do so in a way that
satisfies the following conditions:

 #. A minimum of source code is changed.
 #. There are no deep hacks which are not trivial to explain when taken one by
    one.
 #. The caller may use either the Twisted or non-Twisted interfaces at their
    leisure.
 #. The difference between the Twisted and non-Twisted results at all of the
    borders of the module should be undone by ``maybeDeferred``.

These conditions should not be difficult to achieve and yet they seem to
constantly stymie many would-be IRC bot authors. I'm going to see if I can
improve on this with a couple lessons from Haskell.

So, first, let's consider why we cannot simply remove data from Twisted
interfaces. It's elementary: ``Deferred`` computations cannot have their
results accessed directly. Instead, actions have to be lifted up into a
``Deferred``, which will run the action when it is ready.

To a Haskell programmer, this sounds quite a bit like how ``IO`` behaves, and
indeed, ``Deferred`` is a ``Functor`` (and ``Monad``) that cannot be
unwrapped. So, with this in mind, let's look a bit at what kind of interface
this would be in Haskell. First, let's consider the type of our computation:

.. sourcecode:: haskell

    computation :: a -> b

That is, we are taking some data of type ``a`` and returning some data of type
``b``. The trick here, for those of you not well-versed in Haskell, is that
``computation`` may not do **anything** outside of these types; it cannot
perform I/O or have any impure effects. (Okay, fine, I mean, you can perform
horrid hacks to do those things, but remember our rules: No deep hackery
here.)

Now, let's consider the type of the Twisted-style computation.

.. sourcecode:: haskell

    deferredComputation :: Deferred a -> Deferred b

That is, we're taking a ``Deferred`` containing data of type ``a``, and
returning a ``Deferred`` with data of type ``b``.

Now, here's the fun part. We want to generate ``deferredComputation`` from
``computation``, to achieve code reuse. How? Well, let's use ``fmap``, since
``Deferred`` is a ``Functor``!

.. sourcecode:: haskell

    computation :: a -> b

    fmap :: Functor f => (a -> b) -> f a -> f b

    deferredComputation :: Deferred a -> Deferred b
    deferredComputation = fmap computation

Hey hey! Pretty cool, right? This might seem super-obvious to people with lots
of Haskell experience, but I think it's still worth repeating since not
everybody has done this sort of thing before.

And now we return to the land of Python. Python-land. It's time to construct
this thing in Python, as well. So, how do we lift a function up into a
``Deferred`` in Python?

.. sourcecode:: python

    def computation(a):
        return b

    def deferredComputation(deferred):
        deferred.addCallback(a)
        return deferred

Think about this for a second. Remember, ``Deferred`` objects carry state
around with them, so we need this "impure" sort of approach, which is really
not actually impure but just object-at-a-time. If you're unsure of exactly
what this snippet's doing, stop and think about it for a bit until you're sure
you've got it down.

Now, let's make this concrete. Let's say that we've got a system that has two
implementations of a client, one which is synchronous, and one which is
asynchronous. We've isolated and split out these clients such that they have
exactly the same setup functions, and they return exactly the same data, with
one single difference: One client is blocking and returns the data, and the
other client is non-blocking and returns a ``Deferred`` which will fire with
the data. This is *exactly* the difference that ``maybeDeferred`` can paper
over. We've got all of the code set up just the way we want it, according to
those conditions I listed earlier.

But! These clients only make up a couple dozen lines of code. There are still
thousands of lines of code that only work with the synchronous client. How do
we make them work with Twisted without losing our synchronous abilities?

Let's create some helper which will **apply** the computation to the data.
This helper will come with the client and will be tailored to the client's
output. For unlifted non-Twisted data, this is simply the classic builtin
``apply``, known to Haskellers as ``($)``:

.. sourcecode:: haskell

    ($) :: (a -> b) -> a -> b
    f $ a = f a

.. sourcecode:: python

    def apply(f, a):
        return f(a)

And for the ``Deferred``-handling case, let's create a slightly more
interesting applier which will continue to move data through the ``Deferred``.
We already wrote this above, actually, and in Haskell, it would be ``fmap``:

.. sourcecode:: python

    fmap :: Functor f => (a -> b) -> f a -> f b

    def deferredApply(f, deferred):
        deferred.addCallback(f)
        return deferred

And now we're ready to put everything together! Here's a small skeleton:

.. sourcecode:: python

    class SyncClient(object):
        applier = staticmethod(apply)

        def request(self, s):
            return sync_library_call(s)

    class AsyncClient(object):
        @staticmethod
        def applier(f, deferred):
            deferred.addCallback(f)
            return deferred

        def request(self, s):
            return async_library_call(s)

    def computation(data):
        transform(data)
        poke(data)
        return data

    def request_and_compute(client, resource):
        data = client.request(resource)
        return client.applier(computation, data)

Look at ``request_and_compute``. It has no idea whether it's handling
synchronous or asynchronous data, and it doesn't really care; it asks the
client to actually apply the computation to the data. And the computation
itself is totally unaware of things going on around it. It doesn't even have
to be pure; it could do all kinds of side effects with that data.

This is the approach I'm taking in a new library I'm hacking together for
`Ganeti`_, called `Gentleman`_. I think it'll work out well.

.. _Ganeti: https://code.google.com/p/ganeti/
.. _Gentleman: https://github.com/MostAwesomeDude/gentleman
.. _Twisted: http://twistedmatrix.com/
