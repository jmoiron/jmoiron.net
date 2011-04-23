#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net main application"""

import os
import re

from flask import Flask

from utils import memoize
from pymongo import Connection

@memoize
def connect(uri):
    """Connect to the uri and return the database object for that uri."""
    pattern = re.compile(r'mongodb://(?P<host>[^:]+):(?P<port>\d+)/(?P<db>\w+)')
    match = pattern.match(uri)
    if not match:
        raise Exception('DB Configuration string "%s" is invalid.' % uri)
    host, port, db = match.groups()
    connection = Connection(host, port)
    return connection[db]

app = Flask('jmoiron.net')

runlevel = os.environ.get('JMOIRON_RUNLEVEL', 'Development')
app.config.from_object('config.%sConfig' % runlevel)

if __name__ == '__main__':
    app.run()

