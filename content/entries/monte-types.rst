title: "Monte: Types"
type: entry
category: entries
datetime: 2015-07-04 18:20:00
---

In type-theoretic terms, `Monte`_ has a very boring type system. All objects
expressible in Monte form a set, **Mont**, which has some properties, but not
anything interesting from a theoretical point of view. I plan to talk about
**Mont** later, but for now we'll just consider it to be a way for me to make
existential or universal claims about Monte's object model.

Let's start with guards. Guards are one of the most important parts of writing
idiomatic Monte, and they're also definitely an integral part of Monte's
safety and security guarantees. They *look* like types, but are they actually
useful as part of a type system?

Let's consider the following switch expression:

.. sourcecode:: monte

    switch (x):
        match c :Char:
            "It's a character"
        match i :Int:
            "It's an integer"
        match _:
            "I don't know what it is!"

The two guards, ``Char`` and ``Int``, perform what amounts to a type
discrimination. We might have an intuition that if ``x`` were to pass
``Char``, then it would not pass ``Int``, and *vice versa*; we might also have
an intuition that the order of checking ``Char`` and ``Int`` does not matter.
I'm going to formalize these and show how strong they can be in Monte.

When a coercion happens, the object being coerced is called the **specimen**.
The result of the coercion is called the **prize**. You've already been
introduced to the **guard**, the object which is performing the coercion.

It happens that a specimen might override a Miranda method, ``_conformTo/1``,
in order to pass guards that it cannot normally pass. We call all such
specimens **conforming**. All specimens that pass a guard also conform to it,
but some non-passing specimens might still be able to conform by yielding a
prize to the guard.

Here's an axiom of guards: For all objects in **Mont**, if some object
``specimen`` conforms to a guard ``G``, and
``def prize := G.coerce(specimen, _)``, then ``prize`` passes ``G``. This
cannot be proven by any sort of runtime assertion (yet?), but any guard that
does not obey this axiom is faulty. One expects that a prize returned from a
coercion passes the guard that was performing the coercion; without this
assumption, it would be quite foolhardy to trust any guard at all!

With that in mind, let's talk about properties of guards. One useful property
is **idempotence**. An idempotent guard ``G`` is one that, for all objects in
**Mont** which pass ``G``, any such object ``specimen`` has the equality
``G.coerce(specimen, _) == specimen``. (Monte's equality, if you're unfamiliar
with it, considers two objects to be equal if they cannot be distinguished by
any response to any message sent at them. I could probably craft equivalency
classes out of that rule at some point in the future.)

Why is idempotency good? Well, it formalizes the intuition that objects aren't
altered when coerced if they're already "of the right type of object." I
expect that if I pass ``42`` to a function that has the pattern ``x :Int``, I
might reasonably expect that ``x`` will get ``42`` bound to it, and not
``420`` or some other wrong number.

Monte's handling of state is impure. This complicates things. Since an
object's internal state can vary, its willingness to respond to messages can
vary. Let's be more precise in our definition of passing coercion. An object
``specimen`` **passes** coercion by a guard ``G`` if, for some combination of
``specimen`` and ``G`` internal states, ``G.coerce(specimen, _) == specimen``.
If ``specimen`` passes for *all* possible combinations of ``specimen`` and
``G`` internal states, then we say that ``specimen`` **always passes**
coercion by ``G``. (And if ``specimen`` cannot pass coercion with any possible
combination of states, then it **never passes**.)

Now we can get to retractability. A idempotent guard ``G`` is
**unretractable** if, for all objects in **Mont** which pass coercion by
``G``, those objects always pass coercion by ``G``. The converse property,
that it's possible for some object to pass but not always pass coercion, would
make ``G`` **retractable**.

An unretractable guard provides a very comfortable improvement over
an idempotent one, similar to dipping your objects in ``DeepFrozen``. I think
that most of the interesting possibilities for guards come from unretractable
guards. Most of the builtin guards are unretractable, too; data guards like
``Double`` and ``Str`` are good examples.

Theorem: An unretractable guard ``G`` partitions **Mont** into two disjoint
subsets whose members always pass or never pass coercion by ``G``,
respectively. The proof is pretty trivial. This theorem lets us formalize the
notion of a guard as protecting a section of code from unacceptable values; if
``Char`` is unretractable (and it is!), then a value guarded by ``Char`` is
always going to be a character and never anything else. This theorem also
gives us our first stab at a type declaration, where we might say something
like "An object is of type Char if it passes Char."

Now let's go back to the beginning. We want to know how ``Char`` and ``Int``
interact. So, let's define some operations analagous to set union and
intersection. The union of two unretractable guards ``G`` and ``H`` is written
``Any[G, H]`` and is defined as an unretractable guard that partitions
**Mont** into the union of the two sets of objects that always pass ``G`` or
``H`` respectively, and all other objects. A similar definition can be created
for the intersection of ``G`` and ``H``, written ``All[G, H]`` and creating a
similar partition with the intersection of the always-passing sets.

Both union and intersection are semigroups on the set of unretractable guards.
(I haven't picked a name for this set yet. Maybe **Mont-UG**?) We can add in
identity elements to get monoids. For union, we can use the hypothetical guard
``None``, which refuses to pass any object in **Mont**, and for intersection,
the completely real guard ``Any`` can be used.

.. sourcecode:: monte

    object None:
        to coerce(_, ej):
            throw(ej, "None shall pass")

It gets better. The operations are also closed over **Mont-UG**, and it's
possible to construct an inverse of any unretractable guard which is also an
unretractable guard:

.. sourcecode:: monte

    def invertUG(ug):
        return object invertedUG:
            to coerce(specimen, ej):
                escape innerEj:
                    ug.coerce(specimen, innerEj)
                    throw(ej, "Inverted")
                catch _:
                    return specimen

This means that we have groups! Two lovely groups. They're both Abelian, too.
Exciting stuff. And, in the big payoff of the day, we get two rings on
**Mont-UG**, depending on whether you want to have union or intersection as
your addition or multiplication.

This empowers a programmer, informally, to intuit that if ``Char`` and ``Int``
are disjoint (and, in this case, they are), then it might not matter in which
order they are placed into the switch expression.

That's all for now!

.. _Monte: http://monte.rtfd.org/
