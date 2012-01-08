#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Forms for admin blog post CRUD."""

from wtforms import *

class PostForm(Form):
    title = TextField('Title', [validators.required])
    is_published = BooleanField('Publish?')
    timestamp = TextField('Timestamp')
    body = TextAreaField('Body', [validators.required])
    #tags = SelectMultipleField('Tags')
    summary = TextAreaField('Summary')


