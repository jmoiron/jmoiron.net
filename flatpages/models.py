#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flatpage models."""

import argot
from micromongo import *

__all__ = ['Flatpage']

class Flatpage(Model):
    collection = 'jmoiron.flatpages'
    spec = {
        'path': Field(required=True, type=basestring),
        'content': Field(required=True, type=basestring),
        'rendered': Field(type=basestring),
    }

    def pre_save(self):
        self.rendered = argot.render(self.content)

