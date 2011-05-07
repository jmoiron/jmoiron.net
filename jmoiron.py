#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net main application"""

import os
import re
import time
import argot

from flask import *
from micromongo import connect, current

# modules from which to build our application
from blog.views import blog
from stream.views import stream
from comments.views import comments

app = Flask(__name__)

runlevel = os.environ.get('JMOIRON_RUNLEVEL', 'Development')
app.config.from_object('config.%sConfig' % runlevel)

connect(app.config['DATABASE_URI'])
dbname = app.config['DATABASE_NAME']

app.register_module(blog, url_prefix='/blog')
app.register_module(stream, url_prefix='/stream')
app.register_module(comments, url_prefix='/comments')

# -- request setup/shutdown --

@app.before_request
def before_request():
    g.db = current()[dbname]
    g.section = filter(None, request.path.split('/'))
    g.section = g.section[0] if g.section else 'index'

@app.after_request
def after_request(response):
    return response

# -- leftover urls --

@app.route('/')
def index():
    from stream.views import index
    return index()

# -- jinja2 filters --

@app.template_filter('pdt')
def pretty_datetime(dt):
    """Show date in a pretty way, similar to new default datetime in django."""
    from utils import utc_to_timezone
    dt = utc_to_timezone(dt, 'US/Eastern')
    return time.strftime('%B %d, %Y, %I:%M %p', dt.timetuple())\
            .replace('AM', 'a.m.')\
            .replace('PM', 'p.m.')

@app.template_filter('argot')
def argot_filter(string):
    return argot.render(str(string))

if __name__ != '__main__':
    db = current()[dbname]

