#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream data access models"""

from flask import render_template
from micromongo import *

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
        self.doc.id = self.objects.find().count() + 1
        self.doc.rendered = self.render()

    def render(self):
        template = "stream/plugins/%s.html" % (self.doc.source_tag)
        return  render_template(template, entry=self.doc)



