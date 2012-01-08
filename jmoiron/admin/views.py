#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Admin views.  These mostly farm out to the registered managers and
modules, but do provide basic navigation scaffolding for a simple CRUD
app."""

from flask import *
from flaskext.login import login_required

from models import admin_manager
from models import blueprint as admin

from jmoiron.utils import Page, json_response, dumps

@admin.route("/")
@login_required
def index():
    return render_template("admin/index.html",
        admin_manager=admin_manager)

@admin.route("/<manager>/")
@login_required
def manager(manager):
    try:
        manager_obj = admin_manager.blueprint_map[manager].admin_manager
    except (KeyError, AttributeError):
        abort(404)

    if not len(manager_obj.modules):
        abort(404)
    if len(manager_obj.modules) == 1:
        return redirect(url_for("admin.list", manager=manager, module=manager_obj.modules[0].name))

    return render_template("admin/manager/index.html",
        admin_manager=admin_manager,
        manager=manager_obj)

@admin.route("/<manager>/<module>/")
@login_required
def list(manager, module):
    try:
        manager_obj = admin_manager.blueprint_map[manager].admin_manager
        module_obj = manager_obj.modmap[module]
    except (KeyError, AttributeError):
        abort(404)

    content = module_obj.list()
    return render_template("admin/module/index.html",
        admin_manager=admin_manager,
        manager=manager_obj,
        module=module_obj,
        content=content)

@admin.route("/<manager>/<module>/add/", methods=("GET", "POST"))
@login_required
def add(manager, module):
    abort(404)

@admin.route("/<manager>/<module>/edit/<id>/", methods=("GET", "POST"))
@login_required
def edit(manager, module, id):
    try:
        manager_obj = admin_manager.blueprint_map[manager].admin_manager
        module_obj = manager_obj.modmap[module]
    except (KeyError, AttributeError):
        abort(404)

    content = module_obj.edit(id)
    return render_template("admin/module/edit.html",
        admin_manager=admin_manager,
        manager=manager_obj,
        module=module_obj,
        content=content)

@admin.route("/<manager>/<module>/delete/", methods=("POST",))
@login_required
def delete(manager, module):
    print request.form
    return redirect(request.referrer)

