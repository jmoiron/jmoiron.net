#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream application views"""

from flask import Module, g, request, render_template

stream = Module(__name__, 'stream')

@stream.route("/")
def index():
    return render_template('stream/index.html', **{})
