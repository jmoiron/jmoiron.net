#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Authentication data models."""

import datetime

from flaskext.login import LoginManager, UserMixin
from micromongo import *

login_manager = LoginManager()


class User(Model):
    collection = 'jmoiron.user'
    spec = {
        'username': Field(required=True),
        'password': Field(required=True),
        'email': Field(required=True),
    }

    def get_id(self):
        return self.username


@login_manager.user_loader
def user_loader(userid):
    try:
        return User.find({'username': userid})[0]
    except:
        return None

