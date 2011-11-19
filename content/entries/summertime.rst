title: Summertime
type: entry
category: entries
datetime: 2011-07-31 23:47:12
---

Some people use summer vacation to do useful things. I have been using my
summertime to demonstrate how awesome Twisted_ is.

Here's a fun example: Take this `basic long-polling example`_, in gevent, and
turn it into a Twisted-based server instead.

First, let's look at the chunk of code that will communicate with the web
browser:

.. sourcecode:: python 

    class Pusher(Resource):

        isLeaf = True

        def render_GET(self, request):
            d = cc.connectTCP("localhost", 6379)
            @d.addCallback
            def cb(protocol):
                protocol.request = request
                protocol.subscribe("messages")

            request.write(" " * 4096)
            request.write("<!DOCTYPE html><h1>Messages!</h1>\n")

            return NOT_DONE_YET

Pretty nifty, right? This is a straightforward Twisted Web resource. It will
respond to GET requests by writing a small banner, "Messages!" and will leave
the connection open via ``NOT_DONE_YET``. It also opens a connection to some
local server via the ``cc`` object, which I will explain momentarily.

Now, let's look at the Redis client. This is my first time ever using Redis,
and also using txRedis, but I think I did alright.

.. sourcecode:: python

    class Puller(RedisSubscriber):

        request = None

        def messageReceived(self, channel, message):
            if self.request and not self.request.finished:
                self.request.write("<div>Message on %s: '%s'</div>\n"
                    % (channel, message))
                if message == "quit":
                    self.request.finish()

            if message == "quit":
                self.transport.loseConnection()

What does this do? I'm not super-sure, but it's pretty self-explanatory,
thankfully. ``RedisSubscriber`` is a protocol which can subscribe to, and
publish, messages on Redis. Only the ``messageReceived`` method needs to be
overriden, and we just use it to send messages to that request object.

Here's the part where people might get lost. How are these two objects hooked
up? Well, the answer (as some of you Twisted veterans may have guessed) is the
venerable ClientCreator_, which creates instances of ``Puller`` for every
GET request made in the ``Pusher``. Now, hopefully, the first half of
``render_GET()`` makes more sense: The ``ClientCreator`` is asked to connect
to the local Redis server on port 6379, and will return a ``Puller`` in the
callback. The ``Pusher`` then hands the request over, and the ``Puller`` will
relay any Redis messages it picks up into that request. Everything else is
plumbing or sanity stuff; of note are the 4KiB of empty space at the beginning
of the request, which convinces browsers to start rendering the page, and also
the logic in ``messageReceived`` for closing the request and transport
properly.

Here's the entire thing, imports and all. Note that it's only one line longer
than the gevent version, and comes with a bunch of nifty free features like
PyPy_ compatibility.

.. sourcecode:: python

    from twisted.internet import reactor
    from twisted.internet.protocol import ClientCreator
    from twisted.web.resource import Resource
    from twisted.web.server import Site, NOT_DONE_YET

    from txredis.protocol import RedisSubscriber

    class Puller(RedisSubscriber):

        request = None

        def messageReceived(self, channel, message):
            if self.request and not self.request.finished:
                self.request.write("<div>Message on %s: '%s'</div>\n"
                    % (channel, message))
                if message == "quit":
                    self.request.finish()

            # Ugh, Venn logic.
            if message == "quit":
                self.transport.loseConnection()

    cc = ClientCreator(reactor, Puller)

    class Pusher(Resource):

        isLeaf = True

        def render_GET(self, request):
            d = cc.connectTCP("localhost", 6379)
            @d.addCallback
            def cb(protocol):
                protocol.request = request
                protocol.subscribe("messages")

            request.write(" " * 4096)
            request.write("<!DOCTYPE html><h1>Messages!</h1>\n")

            return NOT_DONE_YET

    reactor.listenTCP(1234, Site(Pusher()))
    reactor.run()

.. _Twisted: http://twistedmatrix.com/
.. _basic long-polling example: http://toastdriven.com/blog/2011/jul/31/gevent-long-polling-you/
.. _ClientCreator: http://twistedmatrix.com/documents/current/api/twisted.internet.protocol.ClientCreator.html
.. _PyPy: http://pypy.org/
