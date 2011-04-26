#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream application views"""

from flask import Module, g, request, render_template
from models import Entry

stream = Module(__name__, 'stream')

@stream.route("/")
def index():
    entries = Entry.find().order_by('-timestamp')[:25]
    return render_template('stream/index.html', **locals())
