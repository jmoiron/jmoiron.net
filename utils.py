#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""utils for jmoiron.net

a lot of this is lifted from iris.
"""

from uuid import uuid4
from threading import local
from functools import wraps
from flask import g

def memoize(function):
    """Memoizing function.  Potentially not thread-safe, since it will return
    resuts across threads.  Make sure this is okay with callers."""
    _cache = {}
    @wraps(function)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in _cache:
            _cache[key] = function(*args, **kwargs)
        return _cache[key]
    return wrapper

def humansize(bytesize, persec=False):
    """Humanize size string for bytesize bytes."""
    units = ['Bps', 'KBps', 'MBps', 'GBps'] if persec else ['B', 'KB', 'MB', 'GB']
    # order of magnitude
    reduce_factor = 1024.0
    oom = 0
    while bytesize /(reduce_factor**(oom+1)) >= 1:
        oom += 1
    return '%0.2f %s' % (bytesize/reduce_factor**oom, units[oom])

class OpenStruct(local):
    """Ruby style openstruct.  Implemented by myself millions of times.
    Thread local."""
    def __init__(self, *d, **dd):
        if d and not dd:
            self.__dict__.update(d[0])
        else:
            self.__dict__.update(dd)
    def __iter__(self):  return iter(self.__dict__)
    def __getattr__(self, attr): return self.__getitem__(attr)
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return None
    def __setitem__(self, item, value): self.__dict__[item] = value
    def __delitem__(self, item):
        if item in self.__dict__:
            del self.__dict__[item]
    # the rest of the dict interface
    def get(self, key, *args):
        return self.__dict__.get(key, *args)
    def keys(self):  return self.__dict__.keys()
    def iterkeys(self): return self.__dict__.iterkeys()
    def values(self): return self.__dict__.values()
    def itervalues(self): return self.__dict__.itervalues()
    def items(self): return self.__dict__.items()
    def iteritems(self): return self.__dict__.iteritems()
    def update(self, d): self.__dict__.update(d)
    def clear(self): self.__dict__.clear()

wrap = lambda objects: [OpenStruct(obj) for obj in objects]

required = uuid4().hex

class Model(object):
    def __init__(self, *args, **kwargs):
        self.doc = OpenStruct(self.spec)
        if args and not kwargs:
            self.doc.update(args[0])
        else:
            self.doc.update(kwargs)

    def check_spec(self):
        if required in self.doc.values():
            missing = [k for k,v in self.doc.items() if v is required]
            raise Exception("Required fields missing: %s" % (missing))

    def pre_save(self):
        return

    def save(self):
        self.pre_save()
        self.check_spec()
        self.objects.save(dict(self.doc))

class Manager(object):
    def __init__(self, cname):
        self.cname = cname

    def _get_collection(self):
        return g.db[self.cname]
    collection = property(_get_collection)

    def find(self, *args, **kwargs):
        return self.collection.find(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.collection.insert(*args, **kwargs)

    def save(self, *args, **kwargs):
        return self.collection.save(*args, **kwargs)
