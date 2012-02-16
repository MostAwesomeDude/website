title: Be Prepared
type: entry
category: entries
datetime: 2012-02-15 20:34:00
---

I like `Flask`_. No, really, I do. Yesterday, during a lightning talk, I
claimed that I love it, and if I don't love it, then at least I love the form
and function of it. I wouldn't marry it, since I don't think being married to
a microframework for Web applications would provide any tax benefits. Maybe
I'm getting off-topic?

Flask is built on `Werkzeug`_, and directly uses Werkzeug routes for view
lookup and URL building. As a result, anything that can be done to Werkzeug
can be done to Flask. A little-known ability of Werkzeug is the ability to add
new **URL converters**. An example and explanation is provided in the
`Werkzeug documentation on converters`_. I decided to build some cool
converters which would automate some of the work I have to do when working
with certain objects.

Without further ado, I would like to present ``ModelConverter``, a class which
can convert a segment of a URL representing a text field on a model into an
instance of that model, and vice versa.

.. sourcecode:: python

    from __future__ import with_statement

    from werkzeug.routing import BaseConverter, ValidationError

    from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

    class ModelConverter(BaseConverter):
        """
        Converts a URL segment to and from a SQLAlchemy model.

        Rather than use an initializer, this class should be subclassed and
        have the `model` and `field` class attributes filled in. `model` is
        the Flask-SQLAlchemy model to use for queries, and `field` is the
        field on the model to use for lookups.

        The field to use should be Unicode or bytes.
        """

        def to_python(self, value):
            try:
                with self.app.test_request_context():
                    obj = self.model.query.filter_by(**{self.field: value}).one()
            except (MultipleResultsFound, NoResultFound):
                raise ValidationError()

            return obj

        def to_url(self, value):
            return getattr(value, self.field)

This particular flavor uses an inheritance-based approach in order to avoid
clobbering ``BaseConverter``'s initializer, but a compositional approach works
too. A ``make_model_converter`` convenience method can provide the glue needed
to specialize the converter. To apply it to the Flask application, merely
modify the URL map after application creation:

.. sourcecode:: python

    from converters import make_model_converter
    from models import Character

    app = Flask(__name__)

    app.url_map.converters["character"] = make_model_converter(app, Character,
        "slug")

And now you can create cool things along the lines of:

.. sourcecode:: python

    @app.route("/<character:c>")
    def character(c):
        return render_template("character.html", c=c)

There is one caveat with this technique: the model instances retrieved this
way will be detached from SQLAlchemy and the current session will not know
about them. If you need to look up any lazily-loaded data on the models, you
will need to add them to the current session first. For example, assuming
``Character.friends`` is a lazily-loaded one-to-many mapping:

.. sourcecode:: python

    @app.route("/<character:c>/friends")
    def character_and_friends(c):
        db.session.add(c)
        return render_template("friends.html", c=c, friends=c.friends)

Today's snippets are all real-world snippets from `DCoN`_, and can be seen in
the `converters.py`_ and `views.py`_ source files.

.. _Flask: http://flask.pocoo.org/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Werkzeug documentation on converters:
   http://werkzeug.pocoo.org/docs/routing/#custom-converters 
.. _DCoN: https://github.com/MostAwesomeDude/dcon
.. _converters.py:
   https://github.com/MostAwesomeDude/dcon/blob/master/newrem/converters.py
.. _views.py:
   https://github.com/MostAwesomeDude/dcon/blob/master/newrem/views.py
