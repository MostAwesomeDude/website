title: Take a Bow
type: entry
category: entries
datetime: 2011-03-10 05:48:12
---

Over the past few months, I've been working on a new server for Minecraft_,
called Bravo_. I haven't made any blog posts about it, mostly because I
haven't been blogging, but also because, frankly, there hasn't been much to
say about it. Bravo is very featureful and robust, but is not at the level of
the nicer servers, like Mineserver_. However, I mention Bravo and Minecraft
because I am going to outline a Minecraft server exploit which has a familiar
moral which I have been championing lately.

When it comes to networking, thread-per-connection is often considered to be
Baby's First Concurrency Model: It's obvious, and works for very, very small
things, but never scales very far and is quite painful to work with. There are
many other ways to do networking, and properly describing them all would go
beyond the scope of this writeup, but I will mention that they generally are
based on the concept of *multiplexing*: syscalls like ``select()`` or
``poll()`` are used to list a set of connections and figure out which ones are
ready to read from or write to, without extra userspace overhead.

So, let's take a look at the proof-of-concept snippet I have rigged up for
this. For those of you wanting to get a link to the entire proof of concept,
there is a copy on Github_ at
https://github.com/MostAwesomeDude/bravo/blob/master/tools/serverbench.py,
from which this snippet was culled.

.. sourcecode:: python

    class TrickleProtocol(Protocol):
        """
        Implementation of the "trickle" DoS attack on MC servers.
        """

        def __init__(self):
            """
            Prepare our payload.
            """

            self.payload = "\x02\xff\xff" + "".join(
                random.choice(string.printable) for i in range(65335))
            self.index = 0

        def connectionMade(self):
            """
            Send our payload at an excruciatingly slow pace.
            """

            self.loop = LoopingCall(self.sendchar)
            self.loop.start(1)

        def sendchar(self):
            """
            Send a single character down the pipe.
            """

            self.transport.write(self.payload[self.index])
            self.index += 1
            if self.index >= len(self.payload):
                # Just stop and wait to get reaped.
                self.loop.stop()

Wow! So this is a small chunk of Twisted_ code which describes a single
client. If about 400 of these are spawned and thrown at the official
("Notchian") Minecraft Beta multiplayer server, the server stops accepting new
connections. What's going on here?

Well, first, we need to know a bit about Minecraft's wire protocol. Minecraft
uses a very straightforward protocol based on packets. Each packet has a
single-byte header identifying the packet, and then a payload based on the
packet identifier. Not an uncommon pattern for homebrewed networking. Inside
each packet, there is a pre-defined data structure built out of certain
primitives: Bytes, shorts, ints, floats, doubles; as well as more complex
structures, like strings.

How are strings stored on the wire? Well, good question. Since the server is
written in Java, it was decided that the string type would match the
implementation of Java's ``readUTF()`` function, which is documented at
http://download.oracle.com/javase/6/docs/api/java/io/DataInput.html. Looking
at that documentation, we see that strings are UTF-8 encoded into bytes, and
sent length-prefixed, with length always as an unsigned short. This means that
strings are limited in length to 65535 bytes.

Now, how is this used by the Notchian server? Well, the server is
thread-per-connection, so it was figured that it would be a good idea to just
pass the incoming socket directly to ``readUTF()`` and friends, in blocking
mode. What this effectively means is that the thread containing the socket
will block and yield control as needed, until enough bytes have come in to
satisfy ``readUTF()`` and relenquish control back to the server.

Imagine what happens if we were to give ``readUTF()`` a relatively large size,
say, 65535, and then very slowly send characters down the wire to the server.
The server cannot really do much about it since ``readUTF()`` is a library
function; it has to wait until ``readUTF()`` has finished reading the string.
This means that a malicious client could completely tie up a thread by doing
this "slow trickle" of data. If enough threads are tied up, then the server
will be unable to handle new requests because of resource exhaustion.

"But surely," you might say, "That is part of the point of authentication!
Only an authenticated client would be able to send this sort of data, and
since Minecraft is centrally authenticated, this certainly armors Minecraft
servers from this sort of attack." You would be partially correct. Servers do
phone home in order to authenticate players, but before they do that, they
must gather some information from the player. In particular, they need the
player's username and a shared secret. The *very first packet* sent by the
client to the server is 0x02, the handshake packet, which looks roughly like
this:

 * Header: byte 0x02
 * Username: string ...
 * ...

Yeah, that's right, the very first thing the client sends to the server is
capable of exploiting this problem. This should help explain the nature of the
payload: The first three bytes are the packet header and string length, and
the rest is just UTF-8-safe padding to keep the connection alive until reaped.
The Notchian server *does*, to its credit, kill threads for connections that
take too long to log in and get authenticated, but it is in vain, for there is
enough time to easily spawn several thousand connections concurrently and have
them wedge the server.

So what happens when the server receives too many connections? It has a
thread-related error, and not just any error, but the mythical and dreaded
``OutOfMemoryError``, which generally is considered a "PORK CHOP SANDWICHES"
kind of problem which cannot be recovered from, and in this case, the server
doesn't try to do anything. It just rolls over and dies. It still can handle
connections, kind of, but only a small handful from its initial thread pool.

Who does this affect? It definitely affects Mojang's Notchian server, and by
extension, projects like `Bukkit/CraftBukkit`_. It does not affect Bravo, nor
craftd_. Although I haven't tested, I am fairly certain that Mineserver is
also immune.

One thing I heard a few days ago from a Bukkit community member was that the
"1k member limit", or one thousand concurrent connections to a single server,
was some sort of mythical achievement that will take lots of hard work and
careful coding. I am happy to say that Bravo and other properly coded servers
can handle one thousand trickle connections and still allow legitimate players
to connect, log in, and play. The moral of the story is, again: *Don't use
thread-per-connection.* In Java, use NIO_ or MINA_. There are reasonable ways
to do networking in every language; let's start using some of them.

.. _Minecraft: http://minecraft.net/
.. _Bravo: http://bravoserver.org/
.. _Mineserver: http://mineserver.be/
.. _Github: http://github.com/
.. _Twisted: http://twistedmatrix.com/
.. _Bukkit/CraftBukkit: http://bukkit.org/
.. _craftd: https://github.com/kev009/craftd
.. _NIO: http://en.wikipedia.org/wiki/New_I/O
.. _MINA: http://mina.apache.org/
