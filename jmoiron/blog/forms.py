#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms for admin blog post CRUD."""

from wtforms import *

class PostForm(Form):
    title = TextField('Title', [validators.required])
    slug = TextField('Slug', [validators.required])
    is_published = BooleanField('Publish?')
    enable_comments = BooleanField('Enable Comments?')
    timestamp = TextField('Timestamp')
    body = TextAreaField('Body', [validators.required], id="body-field")
    #tags = SelectMultipleField('Tags')
    summary = TextAreaField('Summary')
    # TODO: date, tags, comments


