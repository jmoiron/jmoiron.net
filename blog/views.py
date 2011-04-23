#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""blog views."""

from flask import Module, g, request, render_template

blog = Module(__name__, 'blog')

@blog.route("/")
def index():
    return render_template('blog/index.html', **{})

