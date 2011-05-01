#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""migration helpers."""

import datetime
import simplejson as json

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
    if val is None:
        return val
    if isinstance(val, (basestring, int, long, float, bool)):
        return val
    if isinstance(val, datetime.datetime):
        # strip psycopg2 timezone, store in utc
        return datetime.datetime(*val.utctimetuple()[:6])
    raise Exception("What is this?: %r" % val)

def read_table(table):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM %s;" % table)
    rows = list(cursor)
    for row in rows:
        for r in row.keys():
            row[r] = typemap(row[r])
    return rows

def dstrip(d, *keys):
    """Create a copy of dictionary d, lacking keys."""
    ret = dict(d)
    for key in keys:
        if key in ret:
            del ret[key]
    return ret

class Migrate(object):
    def __init__(self):
        pass

    def stream(self):
        plugins = read_table('stream_streamplugin')
        entries = read_table('stream_streamentry')
        for plugin in plugins:
            plugin['arguments'] = json.loads(plugin['arguments']) if plugin['arguments'] else {}
        for entry in entries:
            entry['data'] = json.loads(entry['data'])
        return dict(plugins=plugins, entries=entries)

    def users(self):
        users = read_table('auth_user')
        return dict(users=users)

    def blog(self):
        posts = read_table("blog_post")
        tags = read_table("tagging_tag")
        tagged_objects = read_table("tagging_taggedobject")
        tags_by_id = dict([(tag['id'], dstrip(tag, 'id')) for tag in tags])
        tags_by_post_id = {}
        for to in tagged_objects:
            tags_by_post_id\
                .setdefault(to['object_id'], [])\
                .append(tags_by_id[to['tag_id']]['slug'])
        comments = read_table("comments_comment")
        comments_by_post_id = {}
        for co in comments:
            comments_by_post_id\
                .setdefault(co['object_id'], [])\
                .append(co['id'])
        for post in posts:
            post['tags'] = tags_by_post_id.get(post['id'], [])
            post['comments'] = comments_by_post_id.get(post['id'], [])
            post['body'] = post['body'].replace('\r\n', '\n')
            post['timestamp'] = post['pub_date']
            del post['pub_date']
        return dict(posts=posts, tags=tags)

    def comments(self):
        bannedips = read_table("comments_bannedipaddress")
        submissions = read_table("comments_commentsubmission")
        comments = read_table("comments_comment")
        for c in comments:
            del c['content_type_id']
            c['url'] = c.pop('website')
            c['timestamp'] = c.pop('submit_date')
            c['object'] = ('blog_post', c.pop('object_id'))
        return locals()

