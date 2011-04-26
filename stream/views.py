#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream application views"""

from flask import *
from models import Entry, Plugin

stream = Module(__name__, 'stream')

per_page = 25

@stream.route("/")
def index():
    entries = Entry.find().order_by('-timestamp')[:per_page]
    return render_template('stream/index.html', **locals())

@stream.route("/page/<int:num>")
def show_page(num):
    total = Entry.find().count()
    begin = (num-1) * per_page
    end = num * per_page
    if begin > total:
        return abort(404)
    entries = Entry.find().order_by('-timestamp')[begin:end]
    has_next = end < total
    has_prev = num > 1
    entries = list(entries)
    print len(entries)
    return render_template('stream/index.html', **{
        'entries': entries,
        'has_next': has_next,
        'has_prev': has_prev,
        'current': num
    })

@stream.route("/source/<tag>")
def show_tag(tag):
    entries = Entry.find({'source_tag': tag}).order_by('-timestamp')[:per_page]
    return render_template('stream/index.html', **locals())

