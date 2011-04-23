#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net script/commands"""

# TODO: this is deprecated, but alternatives are boilerplate-heavy
from werkzeug import script
from run import app, db

def action_flushdb():
    """Flush the database."""
    db.drop_collection('blog')
    db.drop_collection('stream')
    db.drop_collection('flatpages')

def action_migratedb(dumpfile=('')):
    """Run a migration from an SQL database."""
    from misc import migrate
    print 'Reloading database from "%s"...' % dumpfile
    migrate.loaddb(dumpfile)

if __name__ == '__main__':
    script.run()
