#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream data access models"""

from flask import render_template
from micromongo import *

__all__ = ['Entry', 'Plugin']

class Entry(Model):
    collection = 'jmoiron.stream_entry'
    spec = {
        'source_tag' : Field(required=True, type=basestring),
        'title' : Field(required=True, type=basestring),
        'permalink': Field(type=basestring),
        'data': Field(required=True),
        'id': Field(type=int), # legacy
    }

    def pre_save(self):
        self.id = self.find().count() + 1
        self.rendered = self._render()

    def _render(self):
        template = "stream/plugins/%s.html" % (self.source_tag)
        return  render_template(template, entry=self)


class Plugin(Model):
    collection = 'jmoiron.stream_plugin'
    spec = {
        'tag' : Field(required=True, type=basestring),
        'name' : Field(required=True, type=basestring),
        'id' : Field(type=int), # legacy
        'interval' : Field(type=int),
        'arguments': Field(required=True)
    }

