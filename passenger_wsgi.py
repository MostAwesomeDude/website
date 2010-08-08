#!/usr/bin/env python

from __future__ import with_statement

import collections
import glob
import operator
import os
import sys
import time

interpreter = os.path.expanduser("~/local/bin/python")
if sys.executable != interpreter:
    os.execl(interpreter, interpreter, *sys.argv)

import bottle
import mutagen.oggvorbis
import simplejson
import twitter

bottle.debug(True)

title = "Corbin Simpson ~ Most awesome, dude!"

def preamble():
    """Return a dictionary with items used by all views."""
    return {"title": title, "time": time.time()}

def linkify(text):
    """Find and linkify URLs embedded in a chunk of text."""
    words = text.split()
    for i, word in enumerate(words):
        if word.startswith(("http://", "https://")):
            words[i] = '<a href="%s">%s</a>' % (word, word)
    return " ".join(words)

def find_new_entries():
    """Check for new entries, return whether any were found."""
    retval = False
    for entry in glob.glob("*.entry"):
        ctime = os.stat(entry)[8]
        os.rename(entry, "entries/%s-%s" % (ctime, entry))
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
        d["paragraphs"] = [i.strip() for i in f.read().split("\n\n")]

    d["headline"] = d["paragraphs"].pop(0)
    d["paragraphs"] = [linkify(i) for i in d["paragraphs"]]

    return d

@bottle.route("/static/:filename")
def static(filename):
    return bottle.static_file(filename, root="public/static")

@bottle.route("/music/:filename")
def static_music(filename):
    return bottle.static_file(filename, root="music")

@bottle.post("/twitter")
def tweet():
    payload = bottle.request.forms.get("payload")
    payload = simplejson.loads(payload)
    name = payload["repository"]["name"]
    head = payload["ref"].split("/")[-1]
    message = "$ (cd %s; git push github %s)" % (name, head)

    api = twitter.Api(username="corbinsimpson", password=password)
    api.PostUpdate(message)

    return "Shazam!"

@bottle.route("/entry/:name")
@bottle.view("entry")
def entry(name):
    d = preamble()

    try:
        # Get the actual filename in entries/
        entry = glob.glob("entries/*-%s.entry" % name)[0]
        d["entry"] = entry_dict(entry)
    except:
        bottle.abort(404, "The desired entry does not exist.")

    return d

@bottle.route("/")
@bottle.route("/index")
@bottle.route("/index/:page")
@bottle.view("index")
def index(page=0):
    d = preamble()
    d["entries"] = list()
    offset = page * 5

    find_new_entries()

    for f in glob.glob("entries/*.entry"):
        d["entries"].append(entry_dict(f))
    d["entries"].sort(key=lambda x: x["mtime"], reverse=True)
    d["entries"] = d["entries"][offset:offset + 5]

    return d

@bottle.route("/music")
@bottle.view("music")
def music():
    d = preamble()
    d["albums"] = collections.defaultdict(list)

    for name in glob.glob("music/*.ogg"):
        info = mutagen.oggvorbis.OggVorbis(name)
        album = info["album"][0], info["date"][0]
        track = name, info["title"][0], info["tracknumber"][0]
        d["albums"][album].append(track)

    for album in d["albums"].itervalues():
        album.sort(key=operator.itemgetter(2))

    return d

application = bottle.app()

if __name__ == "__main__":
    bottle.run(app=application)
