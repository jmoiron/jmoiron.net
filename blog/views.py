#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""blog views."""

from flask import *
from models import *
from comments.models import Comment

from utils import Page, json_response, dumps

blog = Blueprint('blog', __name__,
    template_folder='templates',
    static_folder='static',
)

per_page = 10

@blog.route("/")
def index():
    return show_page(1)

@blog.route("/page/<int:num>")
def show_page(num):
    p = Page(num, per_page, Post.find().count())
    p.urlfunc = lambda num: url_for('blog.show_page', num=num)
    if not p.exists:
        abort(404)
    posts = Post.find({'is_published': True}).order_by('-timestamp')[p.slice()]
    return render_template('blog/index.html', posts=posts, page=p)

@blog.route("/<slug>")
def detail(slug):
    try:
        post = Post.find({'slug': slug})[0]
    except IndexError:
        abort(404)
    post.load_comments()
    return render_template('blog/detail.html', post=post)

blog_admin = Blueprint(__name__, 'blog_admin')

