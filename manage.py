#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net script/commands"""

from flaskext.script import Manager
from glob import glob

from misc import migrate
from jmoiron.app import app, db

script = Manager(app)

@script.command
def loadsql(dumpfile=None):
    """Reload the SQL database."""
    if dumpfile is None:
        try:
            dumpfile = glob("*.sql")[-1]
        except:
            print "Could not find a dumpfile (*.sql) in CWD."
            return
    migrate.loaddb(dumpfile)

@script.command
def flushdb():
    """Flush the database."""
    db.drop_collection('blog_post')
    db.drop_collection('stream_entry')
    db.drop_collection('stream_plugin')
    db.drop_collection('comment')
    db.drop_collection('banned_ip')
    db.drop_collection('flatpage')
    db.drop_collection('tag')

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
    # remove the flask-login context processor as it messes up rendering
    # templates outside of a regular run-created context
    from flaskext import login
    procs = app.template_context_processors[None]
    if login._user_context_processor in procs:
        procs.remove(login._user_context_processor)

    print 'Flushing current mongo database...'
    flushdb()
    if dumpfile:
        print 'Reloading database from "%s"...' % dumpfile
        migrate.loaddb(dumpfile)
    print 'Migrating stream objects...'
    m = migrate.Migrate()
    stream = m.stream()
    db['stream_entry'].insert(stream['entries'])
    db['stream_plugin'].insert(stream['plugins'])
    print 'Migrating blog posts...'
    blog = m.blog()
    db['tag'].insert(blog['tags'])
    db['blog_post'].insert(blog['posts'])
    print 'Migrating comments...'
    comments = m.comments()
    db['comment'].insert(comments['comments'])
    db['banned_ip'].insert(comments['bannedips'])
    print 'Resetting blog comments to use oids..'
    from jmoiron.blog.models import Post
    mapping = dict([(c['id'], c['_id']) for c in db.comment.find()])
    for post in Post.find({'comments': {'$ne': []}}):
        post.comments = [mapping[c] for c in post['comments']]
        post.save()
    print 'Rerendering entries...'
    rerender_entries()
    print 'Rerendering comments...'
    for c in db['comment'].find():
        c.save()
    print 'Creating indexes...'
    create_indexes()

@script.command
def rerender_entries(source_tag=None):
    """Rerender stream entries."""
    from jmoiron.stream.models import Entry
    if source_tag:
        entries = Entry.find({'source_tag': source_tag})
    else:
        entries = Entry.find()
    for e in entries:
        e.save()

@script.shell
def shell_context():
    from jmoiron.blog.models import Post
    from jmoiron.auth.models import User

    return {
        'app': app,
        'db': db,
        'cache': None,
        'Post': Post,
        'User': User,
    }

if __name__ == '__main__':
    script.run()

