#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""migration helpers."""

import datetime

from fabric.api import local, hide
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

db = connect(database='jmoiron_net')

def loaddb(filename, db='jmoiron_net'):
    with hide('running', 'stdout', 'stderr'):
        def psql(string):
            local('echo "%s" | psql -d postgres' % string)
        psql("DROP DATABASE %s" % db)
        local('psql -d postgres < %s' % (filename))

def typemap(val):
    """Provide type mapping between values that psycopg2 return to us
    and values we might be able to store in mongodb easily."""
    if isinstance(val, (basestring, int, long, float, bool)):
        return val
    if isinstance(val, datetime.datetime):
        pass
    raise Exception("What is this?: %r" % val)

def read_table(table):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM %s;" % table)
    return list(cursor)

