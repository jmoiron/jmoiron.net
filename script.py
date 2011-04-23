#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net script/commands"""

from flaskext.script import Manager
from run import app, db

script = Manager(app)

@script.command
def flushdb():
    """Flush the database."""
    db.drop_collection('blog_posts')
    db.drop_collection('stream_entries')
    db.drop_collection('stream_plugins')
    db.drop_collection('flatpages')
    db.drop_collection('tags')

@script.command
def create_indexes():
    """Create indexes on the mongo collections."""
    import pymongo
    db.stream_entries.create_index('source_tag')
    db.stream_entries.create_index([('timestamp', pymongo.DESCENDING)])
    db.blog_posts.create_index('tags')
    db.blog_posts.create_index([('timestamp', pymongo.DESCENDING)])
    db.tags.create_index('slug')

@script.command
def migratedb(dumpfile=None):
    """Run a migration from an SQL database."""
    from misc import migrate
    print 'Flushing current mongo database...'
    action_flushdb()
    if dumpfile:
        print 'Reloading database from "%s"...' % dumpfile
        migrate.loaddb(dumpfile)
    print 'Migrating stream objects...'
    m = migrate.Migrate()
    stream = m.stream()
    db['stream_entries'].insert(stream['entries'])
    db['stream_plugins'].insert(stream['plugins'])
    print 'Migrating blog posts...'
    blog = m.blog()
    db['tags'].insert(blog['tags'])
    db['blog_posts'].insert(blog['posts'])
    print 'Creating indexes...'
    action_create_indexes()

if __name__ == '__main__':
    script.run()

