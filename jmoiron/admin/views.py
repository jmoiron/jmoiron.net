#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""admin views."""

from flask import *
from flaskext.login import login_required
from models import admin_manager

from jmoiron.utils import Page, json_response, dumps

admin = Blueprint('admin', __name__,
    template_folder='templates',
    static_folder='static',
)

@admin.route('/')
@login_required
def index():
    return render_template("admin/index.html", manager=admin_manager)

@admin.route('/<slug>/')
@login_required
def app(slug):
    if slug in admin_manager.installed_apps:
        return render_template("admin/index.html")
    abort(404)
