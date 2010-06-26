#!/usr/bin/env python

from __future__ import with_statement

import collections
import glob
import operator
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import bottle
import mutagen.oggvorbis

bottle.debug(True)

title = "Corbin Simpson ~ Most awesome, dude!"

def linkify(text):
    """Find and linkify URLs embedded in a chunk of text."""
    words = text.split()
    for i, word in enumerate(words):
        if word.startswith(("http://", "https://")):
            words[i] = '<a href="%s">%s</a>' % (word, word)
    return " ".join(words)

def entry_dict(name):
    """Get a template dict from a file name."""
    # Split off .entry
    d = {"name": name[:-6]}

    # os.stat(...)[8] is ctime, [9] is mtime
    stat = os.stat(name)
    d["ctime"] = stat[8]
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

@bottle.route("/entry/:name")
@bottle.view("entry")
def entry(name):
    try:
        d = entry_dict("%s.entry" % name)
        return {"title": title, "entry": d}
    except OSError:
        bottle.abort(404, "The desired entry does not exist.")

@bottle.route("/")
@bottle.route("/index")
@bottle.route("/index/:page")
@bottle.view("index")
def index(page=0):
    d = {"title": title, "entries" : list()}
    offset = page * 5

    for name in glob.glob("*.entry"):
        d["entries"].append(entry_dict(name))
    d["entries"].sort(key=lambda x: x["mtime"])
    d["entries"] = d["entries"][offset:offset + 5]

    return d

@bottle.route("/music")
@bottle.view("music")
def music():
    d = {"title": title, "albums": collections.defaultdict(list)}

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
