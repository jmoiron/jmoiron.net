#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Auth forms."""

from hashlib import md5

from flaskext.wtf import Form, TextField, PasswordField
from flaskext.wtf import Required, Length

from models import User

class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])

    def password_check(self, user=None):
        """Check the password against a user object (or find it in the db).
        If the password check passes, return True.  Otherwise, return False."""
        if self.validate():
            user = user or User.find_one({'username': self.username.data})
            if user and user.password == md5(self.password.data).hexdigest():
                return True
        return False


