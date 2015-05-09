title: Communication on Dictionaries
type: entry
category: entries
datetime: 2015-05-07 14:46:00
---

This post is a reaction to http://blog.rongarret.info/2015/05/why-lisp.html
and I could not think of a better title.

Before I get into my thoughts, I'd like to quickly recap two arguments
presented by two different studiers of communication, as they are essential to
my premise.

The first argument is known as "the medium is the message," from `Marshall
McLuhan`_. It is, in essence, the concept that the *medium* in which a
message is conveyed is part of the message. "Medium" here is the singular of
"media."

The key realization from McLuhan is the idea that, since the message is
inalienably embedded in its medium, the process of interpreting the medium is
*intertwined* with interpreting the message. A message restated in a different
medium is necessarily a different message from the original. It also means
that the ability of a consumer to understand the message is connected to their
ability to understand the medium.

The second argument has no nifty name that I know of. It is `Hofstadter`_'s
assertion, from `GEB`_, that messages are decomposable into (at least) three
pieces, which he calls the *frame*, *outer message*, and *inner message*. The
frame indicates that a message is a message. The outer message explains how
the inner message is structured. The inner message is freeform or formless.

What I'm taking from Hofstadter's model is the idea that, although the frame
can identify a message, neither the frame nor the outer message can actually
explain how the inner message is to be understood. The GEB examples are all
linguistic and describe how no part of a message can explain which language
was used to craft it without using the language in question. The outer message
is the *recognition* that the inner message exists and is in a certain
language.

I can unify these two ideas. I bet that you can, too. McLuhan's medium is
Hofstadter's frame and outer message. A message is not just data, but also the
metadata which surrounds it.

Can we talk about Lisp? Not quite. I have one more thing. Consider two people
speaking English to each other. We have a medium of speech, a frame of
rhythmic audio, and an outer message of English speech. They can understand
each other, right? Well, not quite. They might not speak exactly the same
*dialect* of English. They have different life experiences, which means that
their internal dictionaries, idioms, figures of speech, and so forth might not
line up precisely. As an example, our two speakers might disagree on whether
"raspberry" refers to fruit or flatulence. Worse, they might disagree on
whether "raspberry" refers to berries! These differences constantly occur as
people exchange messages.

Our speakers can certainly negotiate, word by word, any contention, as long as
they have some basic words in common. However, this might not be sufficient,
in the case of some extremely different English dialects like American English
and Scottish English. It also might not be necessary; consider the trope of
two foreigners without a common language coming together to barter or trade,
or the still-not-understood process of linguistic bootstrapping which an
infant performs. Even if the inner message isn't decodable, the outer message
and frame can still carry some of the content of the message (since the medium
is the message!) and communication can still happen in some limited fashion.

I'll now point out that the idea that "normal" communication is not "limited"
is illusory; this sort of impedance mismatch occurs during transmission and
receipt of every message, since the precise concepts that a person carries
with them are ever-changing. A person might not even be able to communicate
effectively with themselves; many people have the surreal, uncanny experience
of reading a note which they have written to themselves only a day or two ago,
and not understanding what the note was trying to convey.

I would like to now postulate an idea. Since the medium is the message and the
deciphering and grokking of messages is imperfect, communication is not just
about deciphering messages, but also about discovering the meaning of the
message via knowledge of the medium and messenger. To put it shortly and
informally, communication is about discovering how others talk, not just about
talking.

Okay! Now we're ready to tackle Lisp. What does Lisp source look like? Well,
it's lots of lists, which contain other lists, and some atoms, and some
numbers. Or, at least, that's what a Lisper sees. Most non-Lispers see
parentheses. Lots of parentheses. Lispers like to talk about how the
parentheses eventually fade away, leaving pure syntax, metasyntax,
metapatterns, and so forth. The language has a simple core, and is readily
extended by macros, which are also Lisp code.

I'll get to macros in a second. First, I want to deal with something from the
original article. "Think about it: to represent hierarchical data you need two
syntactic elements: a token separator and a block delimiter.  In S
expressions, whitespace is the token separator and parens are the block
delimiters.  That's it.  You can't get more minimal than that." I am obligated
to disagree. English, the language of the article, has conventions for
semantic blocks, but they are often ignored, omitted, etc. I speak Lojban,
which at its most formal has no delimiters nor token separators which are
readable to the human eye. Placing spaces in Lojban text is a courtesy to
human readers but not needed by computers. Another programming language,
Forth, has no block delimiters. It also lacks blocks. Also the token separator
is, again, a courtesy; Forth's lexer often reinterprets or ignores whitespace
when asked.

In fact, Lisp's syntax is, well, syntax. While relatively simple when compared
to many languages, Lisp is still structured and retains syntax that would be
completely superfluous were one to speak in the language of digital logic
which computers normally use. To use the language from earlier in this post,
Lisp's syntax is part of its framing; we identify Lisp code precisely by the
preponderance of parentheses. The opening parenthesis signals to both humans
and computers alike that a Lisp list is starting.

The article talks about the power to interleave data and code. Code operates
on data. Code which is also data can be operated on by metacode, which is also
code. A strange loop forms. This is not unlike Hofstadter's suggestion that an
inner message could itself contain another outer and inner message. English
provides us with ample opportunities to form and observe such loops. Consider
this quote: "Within these quotation marks, a new message is possible, which
can extend beyond its limits and be interpreted differently from the rest of
the message: 'Within these quotation marks, a new message is possible.'" I've
decided to not put any nasty logic puzzles into this post, but if I had done
so, this would be the spot. Mixing metalevels can be hard.

I won't talk about quoting any longer, other than to note that it's not
especially interesting if a system supports quoting. There is a proof that
`quines` are possible in any sufficiently complex (Turing complete, for
example) language.

Macros are a kind of code-as-data system which involves reflection and
reification, transforming code into data and operating on it before turning
the data back into code. In particular, this permits code to generate code.
This isn't a good or bad thing. In fact, similar systems are seen across the
wider programming ecosystem. C has macros, C++ has templates, Haskell has
Template Haskell, object-based systems like Python, Ruby, and JS have
metaclass or metaprototype faculties.

Lispers loudly proclaim that macros benefit the expressive power of their
code. By adding macros to Lisp code, the code becomes more expressive as it
takes on deeper metalevels. This is not unlike the expressive power that code
gains as it is factored and changed to be more generic. However, it comes at a
cost; macros create *dialects*.

This "dialect" label could be borrowed from the first part of this post, where
I used it to talk about spoken languages. Lispers use it to talk about
different Lisps which have different macros, different builtin special forms,
etc. Dialects create specialization, both for the code and for those reading
and writing the code. This specialization is a direct result of the macros
that are incorporated into the dialect.

I should stress that I am not saying that macros are bad. This metapower is
neither Good nor Bad, in terms of Quality; it is merely different. Lisp is an
environment where macros are accepted. Forth is another such environment; the
creator of Forth anticipated that most Forth code would not be ANS FORTH but
instead be customized heavily for "the task at hand." A Forth machine's
dictionary should be full of words which were created by the programmer
specifically for the programmer's needs and desires.

Dialects are evident in many other environments. Besides Forth and Lisp,
dialects can be seen in large C++ and Java codebases, where tooling and
support libraries make up non-trivial portions of applications. Haskellers are
often heard complaining about lenses and Template Haskell magic. Pythonistas
tell horror stories of Django, web2py, and Twisted. It's not enough to know a
language to be effective in these codebases; it's often necessary to know the
precise dialect being used. Without the dialect, a programmer has to infer
more meaning from the message; they have to put more effort into deciphering
and grokking.

"Surely macros and functions are alike in this regard," you might say, if you
were my inner voice. And you would be somewhat right, in that macros and
functions are both code. The difference is that a macro is metacode; it is
code which operates on code-as-data. This necessarily means that usage of a
macro makes every reader of the code change how they interpret the code; a
reader must either internalize the macro, adding it to their dictionary, or
else reinterpret every usage of the macro in terms of concepts that they
already know. (I am expecting a sage nod from you, reader, as you reflect upon
instances in your past when you first learned a new word or phrase!) Or, to
put it in the terms of yore, the medium is the message, and macros are part of
the medium of the inner message. The level of understanding of the reader is
improved when they know the macros already!

How can we apply this to improve readability of code? For starters, consider
writing code in such a way that quotations and macro applications are
explicit, and that it is obvious which macros are being applied to quotations.
To quote a great programmer, "Namespaces are one honking great idea." Anything
that helps isolate and clarify metacode is good for readability.

Since I'm obligated to mention Monte, I'm going to point out that Monte has a
very clever and simple way to write metacode: Monte requires metacode to be
called with special quotation marks, and also to be annotated with the name of
the dialect to use. This applies to regular expressions, parser generators,
XML and JSON, etc.; if a new message is to be embedded inside Monte code, and
it should be recognized as such, then Monte provides a metacode system for
doing precisely that action. In Monte, this system is called the quasiliteral
system, and it is very much like quasiliteral quoting within Lisp, with the
two differences I just mentioned: Special quotation marks and a dialect
annotation.

I think that that's about the end of this particular ramble. Thanks.

.. _`Marshall McLuhan`: http://en.wikipedia.org/wiki/Marshall_McLuhan
.. _`Hofstadter`: http://en.wikipedia.org/wiki/Douglas_Hofstadter
.. _`GEB`: http://en.wikipedia.org/wiki/Gödel,_Escher,_Bach
.. _`quines`: http://en.wikipedia.org/wiki/Quine_(computing)
