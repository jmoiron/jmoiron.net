#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream data access models"""

from flask import g
from utils import Model, Manager, required

class Entry(Model):
    spec = {
        'source_tag' : required,
        'title' : None,
        'permalink': None,
        'data': None,
        'id': 0,
    }
    objects = Manager('stream_enties')

    def pre_save(self):
        self.doc.id = self.objects.find().count() + 1



