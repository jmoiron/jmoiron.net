#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""blog data models."""

import datetime
import argot
from jmoiron.utils import summarize

from flask import Blueprint, render_template
from micromongo import *

__all__ = ["Post", "blueprint", "url_prefix"]

blueprint = Blueprint("blog", __name__,
    template_folder="templates",
    static_folder="static",
)

url_prefix = "/blog"

class Post(Model):
    collection = "jmoiron.blog_post"
    spec = {
        "title": Field(required=True, default=""),
        "slug": Field(required=True, default=""),
        "body": Field(required=True, default=""),
        "tags": Field(required=True, default=[]),
        "comments": Field(required=True, default=[]),
        "is_published": Field(required=True, default=False, type=bool),
        "summary": Field(),
        "id": Field(required=True, type=int),
        "timestamp": Field(required=True),
    }

    def pre_save(self):
        if not self.id:
            self.id = Post.find().count()
        if not self.timestamp:
            self.timestamp = datetime.now()
        # make sure we undo any comment loading we might have done
        if self.comments and isinstance(self.comments[0], Model):
            self.comments = [c["_id"] for c in self.comments]
        self.rendered = argot.render(self.body)
        self.summary = summarize(self.rendered)

    def load_comments(self):
        """Load comment documents into self.comments rather than oid refs.
        Saving the post reverts this, but be careful not to modify the object"s
        comments after you"ve done this."""
        from jmoiron.comments.models import Comment
        oidmap = Comment.for_objects(self)
        self.comments = [oidmap[c] for c in self.comments]

