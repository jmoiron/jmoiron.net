#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""blog data models."""

import datetime
import argot
from utils import summarize

from flask import render_template
from micromongo import *

__all__ = ['Post']

class Post(Model):
    collection = 'jmoiron.blog_post'
    spec = {
        'title': Field(required=True, default=''),
        'slug': Field(required=True, default=''),
        'body': Field(required=True, default=''),
        'tags': Field(required=True, default=[]),
        'comments': Field(required=True, default=[]),
        'is_published': Field(required=True, default=False, type=bool),
        'summary': Field(),
        'id': Field(required=True, type=int),
        'timestamp': Field(required=True),
    }

    def pre_save(self):
        if not self.id:
            self.id = Post.find().count()
        if not self.timestamp:
            self.timestamp = datetime.now()
        self.rendered = argot.render(self.body)
        self.summary = summarize(self.rendered)

