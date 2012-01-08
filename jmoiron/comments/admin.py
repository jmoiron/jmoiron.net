#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Admin modules for comments."""

from flask import *
from flaskext.wtf import *
from jmoiron.admin.models import Manager, Module

from models import *

admin = Manager(blueprint)

@admin.register("summary")
def summary():
    """Display a summary table of posts as the default dashboard view of the
    blog admin."""
    return comment_list(count=7)

comment = Module("comment")

@comment.register("summary")
def comment_summary():
    return comment_list(count=10)

@comment.register("list")
def comment_list(count=25):
    comments = Comment.find().order_by("-timestamp")[:count]
    module = comment
    return render_template("comments/admin/comment_summary.html", **locals())


admin.add_module(comment)
