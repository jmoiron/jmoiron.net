#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net main application"""

import os
import re
import time
import argot

from flask import *
from micromongo import connect, current

# "blueprints" from which to build our application
from blog.views import blog
from stream.views import stream
from comments.views import comments
from flatpages.views import flatpage

app = Flask(__name__)

runlevel = os.environ.get('JMOIRON_RUNLEVEL', 'Development')
app.config.from_object('config.%sConfig' % runlevel)

connect(app.config['DATABASE_URI'])
dbname = app.config['DATABASE_NAME']

app.register_blueprint(blog, url_prefix='/blog')
app.register_blueprint(stream, url_prefix='/stream')
app.register_blueprint(comments, url_prefix='/comments')

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

@app.errorhandler(404)
def page_not_found(e):
    return "HTTP 404: page not found", 404

# flatpages
app.register_blueprint(flatpage)

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

