#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream application views"""

from flask import *
from models import Entry, Plugin
from utils import Page, json_response, dumps

stream = Module(__name__, 'stream')

per_page = 25

@stream.route("/")
def index():
    return show_page(1)

@stream.route("/page/<int:num>")
def show_page(num):
    p = Page(num, per_page, Entry.find().count())
    if not p.exists:
        abort(404)
    p.urlfunc = lambda n: url_for('stream.show_page', num=n)
    entries = Entry.find().order_by('-timestamp')[p.slice()]
    return render_template('stream/index.html', entries=entries, page=p)

@stream.route("/source/<tag>")
def show_tag(tag):
    entries = Entry.find({'source_tag': tag}).order_by('-timestamp')[:per_page]
    if not entries:
        abort(404)
    return render_template('stream/index.html', **locals())

@stream.route("/ajax/page/<int:num>")
@json_response
def ajax_page(num):
    p = Page(num, per_page, Entry.find().count())
    if not p.exists:
        abort(404)
    entries = Entry.find().order_by('-timestamp')[p.slice()]
    return dumps([e.rendered for e in entries], indent=2, sort_keys=True)

