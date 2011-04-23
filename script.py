#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net script/commands"""

# TODO: this is deprecated, but alternatives are boilerplate-heavy
from werkzeug import script
from run import app, db

def action_flushdb():
    """Flush the database."""
    pass

def action_migratedb(dumpfile=('')):
    """Run a migration from an SQL dumpfile."""
    from misc import migrate
    print dumpfile

if __name__ == '__main__':
    script.run()
