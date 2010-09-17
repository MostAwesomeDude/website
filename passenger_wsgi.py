#!/usr/bin/env python

from __future__ import with_statement

import collections
import datetime
import glob
import operator
import os
import sys
import time

interpreter = os.path.expanduser("~/local/bin/python")
if sys.executable != interpreter:
    os.execl(interpreter, interpreter, *sys.argv)

import docutils.core
import flask
import lxml.html
import lxml.html.clean
import mutagen.oggvorbis
import pygments
import pygments.lexers
import pygments.formatters
import PyRSS2Gen
import simplejson
import twitter
import werkzeug
import werkzeug.contrib.cache

cache = werkzeug.contrib.cache.SimpleCache()

app = flask.Flask(__name__)
app.use_x_sendfile = False

title = "Corbin Simpson ~ Most awesome, dude!"

@app.context_processor
def preamble():
    """
    Return a dictionary with items used by all views.

    The decorator on this function's declaration makes its return values
    become injected into all Jinja contexts.
    """

    return {
        "datetime": datetime,
        "time": time,

        "title": title,
        "starting_time": time.time(),
    }

@app.template_filter()
def rst(s):
    """
    Convert a ReST string to an HTML fragment.
    """

    return docutils.core.publish_parts(s, writer_name="html")["html_body"]

def find_new_entries():
    """Check for new entries, return whether any were found."""
    retval = False
    for entry in glob.glob("*.entry"):
        ctime = os.stat(entry)[8]
        os.rename(entry, "entries/%s-%s" % (ctime, entry))

        message = "$ vi blog/%s ; echo \"Updated my blog. See %s\""
        url = flask.url_for("entry", name=entry[:-6], _external=True)
        message = message % (entry, url)
        tweet(message)
        retval = True
    return retval

def entry_dict(name):
    """
    Get a template dict from a file name.

    Raises various exceptions if it cannot find the requested entry.
    """

    chaff, filename = name.split("/", 1)
    ctime, entry_name = filename.split("-", 1)

    # Split off .entry
    d = {"name": entry_name[:-6]}

    # os.stat(...)[8] is ctime, [9] is mtime
    stat = os.stat(name)
    d["ctime"] = int(ctime)
    d["mtime"] = stat[9]

    with open(name, "r") as f:
        paragraphs = [i.strip() for i in f.read().split("\n\n") if i]

    d["headline"] = paragraphs.pop(0)
    d["paragraphs"] = []

    for paragraph in paragraphs:
        try:
            element = lxml.html.fragment_fromstring(paragraph)
            # Highlight <code class="..."> paragraphs
            if element.tag == "code" and "class" in element.attrib:
                try:
                    lex = pygments.lexers.get_lexer_by_name(
                        element.attrib["class"])
                    element = lxml.html.fragment_fromstring(
                        pygments.highlight(element.text, lex,
                            pygments.formatters.HtmlFormatter()))
                except pygments.util.ClassNotFound:
                    pass
        except lxml.etree.ParserError:
            element = lxml.html.fragment_fromstring(paragraph,
                create_parent="p")

        lxml.html.clean.autolink(element)
        d["paragraphs"].append(lxml.html.tostring(element))

    return d

def tweet(message):
    """
    Publish a message to Twitter.
    """

    oauth = twitter.OAuth(token_key, token_secret,
        consumer_key, consumer_secret)
    try:
        twitter.Twitter(auth=oauth).statuses.update(status=message)
    except twitter.TwitterError, e:
        app.logger.error(e)

@app.route("/static/music/<filename>")
def static_music(filename):
    return flask.send_from_directory("music", filename)

@app.route("/static/<filename>")
def static(filename):
    return flask.send_from_directory("public/static", filename)

@app.route("/twitter", methods=["POST"])
def github_tweet():
    payload = flask.request.form["payload"]
    payload = simplejson.loads(payload)
    name = payload["repository"]["name"]
    head = payload["ref"].split("/")[-1]
    message = "$ (cd %s; git push github %s)" % (name, head)

    tweet(message)

    return "Shazam!"

@app.route("/entry/<name>")
def entry(name):
    d = {}

    try:
        # Get the actual filename in entries/
        entry = glob.glob("entries/*-%s.entry" % name)[0]
        d["entry"] = entry_dict(entry)
    except:
        flask.abort(404, "The desired entry does not exist.")

    return flask.render_template("entry.html", **d)

def get_entries():
    entries = cache.get("entries")
    if find_new_entries() or not entries:
        entries = [entry_dict(f) for f in glob.glob("entries/*.entry")]
        entries.sort(key=lambda x: x["mtime"], reverse=True)
        cache.set("entries", entries)

    return entries

@app.route("/rss.xml")
def rss():
    entries = get_entries()

    items = []
    for entry in entries:
        url = flask.url_for("entry", name=entry["name"], _external=True)
        items.append(PyRSS2Gen.RSSItem(
            title=entry["headline"],
            link = url,
            guid = PyRSS2Gen.Guid(url),
            description = entry["paragraphs"][0],
            pubDate = datetime.datetime.fromtimestamp(entry["ctime"])
        ))
    rss = PyRSS2Gen.RSS2(
        title=title,
        link=flask.url_for("index"),
        description="Party on, dudes!",
        lastBuildDate=datetime.datetime.now(),
        items=items
    )
    return rss.to_xml()


@app.route("/")
@app.route("/index")
@app.route("/index/<page>")
def index(page=0):
    d = {}
    d["entries"] = list()
    offset = page * 5

    entries = get_entries()

    d["entries"] = entries[offset:offset + 5]

    return flask.render_template("index.html", **d)

@app.route("/music")
def music():
    d = {}
    d["albums"] = collections.defaultdict(list)

    for name in glob.glob("music/*.ogg"):
        info = mutagen.oggvorbis.OggVorbis(name)
        album = info["album"][0], info["date"][0]
        track = name[6:], info["title"][0], info["tracknumber"][0]
        d["albums"][album].append(track)

    for album in d["albums"].itervalues():
        album.sort(key=operator.itemgetter(2))

    return flask.render_template("music.html", **d)

@app.route("/cst")
def redirect_cst():
    return flask.redirect(flask.url_for("cst"), 301)

@app.route("/copious-spare-time")
def cst():
    f = open("cst.rst", "r")
    d = {"content": f.read()}

    f.close()

    return flask.render_template("cst.html", **d)

if __name__ == "__main__":
    app.run(debug=True)
else:
    application = app
    import logging
    handler = logging.FileHandler("error.log")
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)
