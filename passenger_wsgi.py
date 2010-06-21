#!/usr/bin/env python

from __future__ import with_statement

import glob
import os

import bottle

bottle.debug(True)

title = "Corbin Simpson ~ Most awesome, dude!"

def entry_dict(name):
    """Get a template dict from a file name."""
    # Split off .entry
    d = {"name": name[:-6]}

    # os.stat(...)[8] is mtime, [9] is ctime
    stat = os.stat(name)
    d["mtime"] = stat[8]
    d["ctime"] = stat[9]

    with open(name, "r") as f:
        d["paragraphs"] = [i.strip() for i in f.read().split("\n\n")]
        d["headline"] = d["paragraphs"].pop(0)

    return d

@bottle.route("/static/:filename")
def static(filename):
    return bottle.static_file(filename, root="static")

@bottle.route("/entry/:name")
@bottle.view("entry")
def entry(name):
    try:
        d = entry_dict("%s.entry" % name)
        return {"title": title, "entry": d}
    except OSError:
        bottle.abort(404, "The desired entry does not exist.")

@bottle.route("/")
@bottle.view("index")
def index():
    d = {"title": title, "entries" : list()}
    for name in glob.glob("*.entry"):
        d["entries"].append(entry_dict(name))
    d["entries"].sort(key=lambda x: x["mtime"])
    return d

bottle.run()
