#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream application views"""

import pymongo

from flask import Module, g, request, render_template

from utils import wrap
from models import Entry

stream = Module(__name__, 'stream')

@stream.route("/")
def index():
    entries = wrap(Entry.objects.find(sort=[('timestamp', pymongo.DESCENDING)])[:25])
    return render_template('stream/index.html', **locals())
