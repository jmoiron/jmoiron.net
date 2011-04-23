#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net fabfile"""

from datetime import datetime
from fabric.api import *
env.hosts = ['jmoiron.net']

def backup_db(db='jmoiron_net'):
    """Dump db and fetch db from the server."""
    # TODO: this fetches the old db, make it fetch the new one
    timestamp = datetime.now().isoformat().split('T')[0]
    path = '/tmp/%s.%s.sql' % (db, timestamp)
    cmd = 'pg_dump -U jmoiron -dCE utf8 %s -f "%s"' % (db, path)
    run(cmd)
    run('gzip "%s"' % path)
    get(path + '.gz', './')
    run('rm "%s.gz"' % path)
    # remove it if it already exists
    local('rm -f %s.%s.sql' % (db, timestamp))
    local('gzip -d %s.%s.sql.gz' % (db, timestamp))

backup_legacy_db = backup_db

