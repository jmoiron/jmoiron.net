#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""comment data models."""

import datetime
import argot
from utils import summarize

from flask import render_template
from micromongo import *

__all__ = ['Post']

class Comment(Model):
    collection = 'jmoiron.comment'
    spec = {
        'comment': Field(required=True, default='', type=str),
        'url': Field(require=True, default='', type=str),
        'email': Field(required=True, default=''),
        'name': Field(required=True, default='', type=str),
        'ip_address': Field(required=True, type=str),
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

