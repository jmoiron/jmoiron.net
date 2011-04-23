#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net main application"""

import os
import re

from flask import Flask, g
from utils import memoize
from pymongo import Connection

# modules from which to build our application
from blog.views import blog
from stream.views import stream

@memoize
def connect(uri):
    """Connect to the uri and return the database object for that uri."""
    pattern = re.compile(r'mongodb://(?P<host>[^:]+):(?P<port>\d+)/(?P<db>\w+)')
    match = pattern.match(uri)
    if not match:
        raise Exception('DB Configuration string "%s" is invalid.' % uri)
    host, port, db = match.groups()
    port = int(port)
    try:
        connection = Connection(host, port)
    except:
        print 'Connection to "%s" failed.' % uri
        raise
    return connection[db]

app = Flask(__name__)

runlevel = os.environ.get('JMOIRON_RUNLEVEL', 'Development')
app.config.from_object('config.%sConfig' % runlevel)
app.register_module(blog, url_prefix='/blog')
app.register_module(stream)

@app.before_request
def before_request():
    g.db = connect(app.config['DATABASE_URI'])

@app.after_request
def after_request(response):
    return response

if __name__ == '__main__':
    app.run()
else:
    db = connect(app.config['DATABASE_URI'])

