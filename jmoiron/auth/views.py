#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Auth views."""

from flask import *
from flaskext import login as flask_login

from models import *
from models import blueprint as auth

from forms import LoginForm

@auth.route("/login", methods=("GET", "POST"))
def login():
    """Log the user in or display the login form."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_one({"username": form.username.data})
        if form.password_check(user):
            flask_login.login_user(user)
            url = request.args.get("next", "/")
            return redirect(url)
    return render_template("auth/login.html", form=form)

@auth.route("/logout")
def logout():
    """Log the user out.  Redirect to the "next" param or to the login page
    regardless of whether or not the user was logged at all or not."""
    if not flask_login.current_user.is_authenticated():
        return redirect(request.args.get("next", url_for("auth.login")))
    user = flask_login.current_user
    flask_login.logout_user()
    return redirect(request.args.get("next", url_for("auth.login")))


