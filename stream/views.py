#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream application views"""

from flask import *
from models import Entry, Plugin
from utils import Page

stream = Module(__name__, 'stream')

per_page = 25

@stream.route("/")
def index():
    p = Page(1, per_page, Entry.find().count())
    p.urlfunc = lambda n: url_for('stream.show_page', num=n)
    entries = Entry.find().order_by('-timestamp')[p.slice()]
    return render_template('stream/index.html', entries=entries, page=p)

@stream.route("/page/<int:num>")
def show_page(num):
    total = Entry.find().count()
    p = Page(num, per_page, total)
    p.urlfunc = lambda n: url_for('stream.show_page', num=n)
    entries = Entry.find().order_by('-timestamp')[p.slice()]
    return render_template('stream/index.html', entries=entries, page=p)

@stream.route("/source/<tag>")
def show_tag(tag):
    entries = Entry.find({'source_tag': tag}).order_by('-timestamp')[:per_page]
    return render_template('stream/index.html', **locals())

