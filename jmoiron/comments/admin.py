#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Admin modules for comments."""

from flask import *
from flaskext.wtf import *
from jmoiron.utils import Page
from jmoiron.admin.models import Manager, Module

from models import *

admin = Manager(blueprint)

@admin.register("summary")
def summary():
    """Display a summary table of posts as the default dashboard view of the
    blog admin."""
    return comment_summary(count=5)

comment = Module("comment")

@comment.register("summary")
def comment_summary(count=10):
    comments = Comment.find().order_by("-timestamp")[:count]
    module = comment
    return render_template("comments/admin/comment_summary.html", **locals())

@comment.register("list")
def comment_list(count=25):
    page = Page(int(request.args.get('page', 1)), count, Comment.find().order_by("-timestamp").count())
    comments = Comment.find().order_by("-timestamp")[page.slice()]
    module = comment
    return render_template("comments/admin/comment_list.html", **locals())


admin.add_module(comment)
