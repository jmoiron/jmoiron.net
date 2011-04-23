#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream data access models"""

from flask import g, render_template
from utils import Model, Manager, required

class Entry(Model):
    spec = {
        'source_tag' : required,
        'title' : None,
        'permalink': None,
        'data': None,
        'id': 0,
    }
    objects = Manager('stream_entries')

    def pre_save(self):
        self.doc.id = self.objects.find().count() + 1
        self.doc.rendered = self.render()

    def render(self):
        template = "stream/plugins/%s.html" % (self.doc.source_tag)
        return  render_template(template, entry=self.doc)



