#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""comment data models."""

import datetime
import argot
import operator

from jmoiron.utils import summarize

from flask import render_template
from micromongo import *
from micromongo.models import class_router

__all__ = ['Comment']

class Comment(Model):
    collection = 'jmoiron.comment'
    spec = {
        'comment': Field(required=True, default='', type=basestring),
        'url': Field(required=True, default='', type=basestring),
        'email': Field(required=True, default=''),
        'name': Field(required=True, default='', type=basestring),
        'ip_address': Field(required=True, type=basestring),
        'timestamp': Field(required=True),
        'needs_moderation': Field(required=True, default=False, type=bool),
        'id': Field(required=True, type=int),
        'object': Field(required=True), # probably a tuple, (collection, _id)
    }

    def pre_save(self):
        if not self.id:
            self.id = Comment.find().count()
        if not self.timestamp:
            self.timestamp = datetime.now()
        self.rendered = argot.render(self.comment)

    @classmethod
    def for_objects(cls, *objects):
        """For a bunch of objects that have a 'comments', replace the oids in
        their lists with the actual embedded comment objects.  Returns the oid
        mapping for comments."""
        oids = reduce(operator.add, [o.get('comments', []) for o in objects])
        comments = cls.find({'_id': {'$in': oids}})
        return dict([(c._id, c) for c in comments])
