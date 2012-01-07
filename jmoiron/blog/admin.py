#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Admin modules for the blog."""

from flask import *
from flaskext.wtf import *
from jmoiron.admin.models import Manager, Module

from models import *

admin = Manager(blueprint)

@admin.register("summary")
def summary():
    """Display a summary table of posts as the default dashboard view of the
    blog admin."""
    return post_summary(count=5)

post = Module("post")

@post.register("summary")
def post_summary(count=8):
    return post_list(count=8)

@post.register("list")
def post_list(count=20):
    posts = Post.find({"is_published": True}).order_by("-timestamp")[:count]
    module = post
    return render_template("blog/admin/post_summary.html", **locals())

admin.add_module(post)



