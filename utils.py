#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""utils for jmoiron.net."""

from math import ceil
from lxml import html
from flask import make_response
from functools import wraps
from simplejson import dumps as json_dumps
from datetime import datetime
from micromongo import Model
from pymongo.objectid import ObjectId

def humansize(bytesize, persec=False):
    """Humanize size string for bytesize bytes."""
    units = ['Bps', 'KBps', 'MBps', 'GBps'] if persec else ['B', 'KB', 'MB', 'GB']
    # order of magnitude
    reduce_factor = 1024.0
    oom = 0
    while bytesize /(reduce_factor**(oom+1)) >= 1:
        oom += 1
    return '%0.2f %s' % (bytesize/reduce_factor**oom, units[oom])

def summarize(string):
    """Summarize a bunch of html.

    What 'summarize' means in this case is to cherrypick the first paragraph
    as well as, if it precedes that tag, the first image tag."""
    soup = html.fragments_fromstring(string)
    ret = []
    for tag in soup:
        if tag.tag == 'img':
            ret.append(html.tostring(tag, method='xml'))
        elif tag.tag == 'p':
            ret.append(html.tostring(tag))
            break
    return '\n'.join(ret)

# -- json utils -- 

def json_response(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        ret = view(*args, **kwargs)
        if isinstance(ret, basestring):
            resp = make_response(ret)
            resp.headers['ContentType'] = 'application/json'
            return resp
        return ret
    return wrapped

def _json_handler(obj):
    if isinstance(obj, datetime):
        return 'new Date("%s")' % obj.ctime()
    if isinstance(obj, Model):
        return dumps(dict(obj))
    if isinstance(obj, ObjectId):
        return json_dumps(str(obj))
    return json_dumps(obj)

@wraps(json_dumps)
def dumps(*args, **kwargs):
    kwargs['default'] = _json_handler
    return json_dumps(*args, **kwargs)

# -- pagination --

class Page(object):
    def __init__(self, number, per_page, total_objects, window=8, urlfunc=None,
            inter='...'):
        self.number = number
        self.per_page = per_page
        self.begin_offset = (number-1) * per_page
        self.end_offset = number * per_page
        self.exists = total_objects > self.begin_offset
        self.has_prev = number > 1
        self.has_next = self.end_offset < total_objects
        self.num_pages = (total_objects / per_page)
        self.num_pages += 1 if (total_objects % per_page) else 0
        self.window = window
        self.urlfunc = None
        self.inter = inter

    def slice(self):
        """Return a slice representing the current page's objects in an object
        list or stream.  Most ORMs will allow slicing for limit/offset."""
        return slice(self.begin_offset, self.end_offset)

    def context(self):
        """Return a page's context, which is a list of strings representing
        pages or interspersed ellipses that surround the current page."""
        return page_context(self, window=self.window, total=self.num_pages,
                inter=self.inter)

    def link_for(self, page):
        """Return a link for a particular page, based on urlfunc if available,
        or just the page number if not."""
        if not self.urlfunc:
            return '/%s' % page
        return self.urlfunc(page)

def make_window(center, size):
    """Make a number window of size with the 'center' in the middle."""
    if size % 2:
        lpad = rpad = size/2
    else:
        lpad = size/2 - 1
        rpad = size/2
    return range(center - lpad, center + rpad + 1)


def page_context(page, window=8, total=None, inter='...'):
    """Takes a page (a Page object, or a number w/ total specified) and returns
    a window with `inter` interspersed between the longer gaps in the context.
    """
    if isinstance(page, (int, long)):
        assert(total)
        current = page
    else:
        current = page.number
        if total is None:
            total = page.paginator.num_pages

    # the pad area is the area around the edges of the total window where the
    # ellipsis algorithm would make the page hit the edge anyway.  We pad the
    # window with 2 on either side, which makes the middle (window/2)
    pad_area = 2 + (ceil(float(window - 4)/2))
    middle = window - 4

    if total < window:
        return range(1, total+1)
    if current <= pad_area:
        return range(1, 2 + middle + 1) + [inter, total-1, total]
    if total - pad_area <= current <= total:
        return [1, 2, inter] + range(total - middle - 1, total+1)
    else:
        return [1, 2, inter] + make_window(current, middle) + [inter, total-1, total]

