title: "Mont is a Category"
type: entry
category: entries
datetime: 2015-07-21 14:33:00
---

I've had a lot of thought about **Mont**. (Sorry for the rhymes.) **Mont**,
recall, is the set of all `Monte`_ objects. I have a couple interesting
thoughts on **Mont** that I'd like to share, but the compelling result I hope
to convince readers of is this: **Mont** is a simple and easy-to-think-about
category once we define an appropriate sort of morphism. By "category" I mean
the fundamental building block of `category theory`_, and most of the maths
I'm going to use in this post is centered around that field. In particular,
"morphism" is used in the sense of categories.

I'd like to put out a little lemma from the other day, first. Let us say that
the Monte ``==`` operator is defined as follows: For any two objects in
**Mont**, ``x`` and ``y``, ``x == y`` if and only if ``x`` is ``y``, or for
any message ``[verb, args]`` sendable to these objects, ``M.send(x, verb,
args) == M.send(y, verb, args)``. In other words, ``x == y`` if it is not
possible to distinguish ``x`` and ``y`` by any chain of sent messages. This
turns out to relate to the category definition I give below. It *also* happens
to correlate nicely with the idea of `equivalence`_, in that ``==`` is an
equivalence relation on **Mont**! The proof:

* Reflexivity: For any object ``x``, ``x == x``. The first branch of the
  definition handles this.
* Symmetry: For any objects ``x`` and ``y``, ``x == y`` iff ``y == x``.
  Identity is symmetric, and the second branch is covered by recursion.
* Transitivity: For any objects ``x``, ``y``, and ``z``, ``x == y`` and ``y ==
  z`` implies ``x == z``. Yes, if ``x`` and ``y`` can't be told apart, then if
  ``y`` and ``z`` also can't be told apart it immediately follows that ``x``
  and ``z`` are likewise indistinguishable.

Now, obviously, since objects can do whatever computation they like, the
actual implementation of ``==`` has to be conservative. We generally choose to
be sound and incomplete; thus, ``x == y`` sometimes has false negatives when
implemented in software. We can't really work around this without weakening
the language considerably. Thus, when I talk about **Mont/==**, please be
assured that I'm talking more about the ideal than the reality. I'll try to
address spots where this matters.

Back to categories. What makes a category? Well, we need a set, some
morphisms, and a couple proofs about the behavior of those morphisms. First,
the set. I'll use **Mont-DF** for starters, but eventually we want to use
**Mont**. Not up on my posts? **Mont-DF** is the subset of **Mont** where
objects are *transitively immutable*; this is extremely helpful to us since we
do not have to worry about mutable state nor any other side effect. (We *do*
have to worry about identity, but most of my results are going to be stated as
holding up to equivalence. I am not really concerned with whether there are
two ``42`` objects in **Mont** right now.)

My first (and, spoiler alert, failed) attempt at defining a category was to
use messages as morphisms; that is, to go from one object to another in
**Mont-DF**, send a message to the first object and receive the second object.
Clear, clean, direct, simple, and corresponds wonderfully to Monte's
semantics. However, there's a problem. The first requirement of a category is
that, for any object in the set, there exists an *identity morphism*, usually
called ``1``, from that object to itself. This is a problem in Monte. We can
come up with a message like that for some objects, like good old ``42``, which
responds to ``["add", [0]]`` with ``42``. (Up to equivalence, of course!)
However, for some other objects, like ``object o as DeepFrozen {}``, there's
no obvious methods to use.

The answer is to add a new Miranda method which is not overrideable called
``_magic/0``. (Yes, if this approach would have worked, I would have picked a
better name.) Starting from **Mont-DF**, we could amend all objects to get a
new set, **Mont-DF+Magic**, in which the identity morphism is always
``["_magic", []]``. This neatly wraps up the identity morphism problem.

Next, we have to figure out how to compose messages. At first blush, this is
simple; if we start from ``x`` and send it some message to get ``y``, and then
send another message to ``y`` to get ``z``, then we obviously can get to ``x``
from ``z``. However, here's the rub: There might not be any message directly
from ``x`` to ``z``! We're stuck here. Unlike with other composition
operators, there's no hand-wavey way to compose messages like with functions.
So this is bunk.

However, we can cheat gently and use the free monoid *a.k.a.* the humble list.
A list of messages will work just fine: To compose them, simply catenate the
lists, and the identity morphism is the empty list. Putting it all together,
a morphism from ``6`` to ``42`` might be ``[["multiply", [7]]]``, and we could
compose that with ``[["asString", []]]`` to get ``[["multiply", [7]],
["asString", []]]``, a morphism from ``6`` to ``"42"``. Not shabby at all!

There we go. Now **Mont-DF** is a category up to equivalence. The (very
informally defined) set of representatives of equivalence classes via ``==``,
which I'll call **Mont-DF/==**, is definitely a category here as well, since
it encapsulates the equivalence question. We could alternatively insist that
objects in **Mont-DF** are unique (or that equivalent definitions of objects
*are* those same objects), but I'm not willing to take up that sword this time
around, mostly because I don't think that it's true.

"Hold up," you might say; "you didn't prove that **Mont** is a category, only
**Mont-DF**." Curses! I didn't fool you at all, did I? Yes, you're right. We
can't extend this result to **Mont** wholesale, since objects in **Mont** can
mutate themselves. In fact, **Mont** doesn't really make sense to discuss in
this way, since objects in sets aren't supposed to be mutable. I'm probably
going to have to extend/alter my definition of **Mont** in order to get
anywhere with that.

.. _Monte: http://monte.rtfd.org/
.. _category theory: https://en.wikipedia.org/wiki/Category_theory
.. _equivalence: https://en.wikipedia.org/wiki/Equivalence_relation
