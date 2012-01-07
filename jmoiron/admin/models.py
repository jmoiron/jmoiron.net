#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Admin CRUD."""

from flask import Blueprint

# The Admin app is actually just a thin scaffolding and some utilities
# to assist in navigating quickly around a basic CRUD interface for your
# various flask blueprints.  The top level object is a Manager, in which
# modules and blueprints are registered.
#
# Each blueprint gets its own top-level navigation item and an associated
# module.  The blueprint-level module is only summary/dashboard inclusion
# on the admin index.
#
# Each blueprint also gets sub-modules, which represent CRUD views for each
# of that blueprints models (or whatever you like).  These modules have four
# basic types, and the admin interface has certain ways it will behave with
# each type:
#
#  * list (search & delete)
#  * create
#  * edit
#  * summary/dashboard
#
# The admin is composed like this:
#
#   * /admin/  - shows a single pane with blueprint summaries
#   * /admin/<blueprint>/  - dual pane, module list left module summaries right
#   * /admin/<blueprint>/<module>/ - list view
#   * /admin/<blueprint>/<module>/(add|edit)/ - add/edit 
#

blueprint = Blueprint("admin", __name__,
    template_folder="templates",
    static_folder="static",
)
url_prefix = "/admin"

class Admin(object):
    def __init__(self):
        self.app = None
        self.blueprints = []
        self.config = {}

    def setup_app(self, app):
        self.app = app
        self.blueprint_map = dict(app.blueprints)
        self.blueprint_map.pop("admin", "")
        self.blueprints = self.blueprint_map.values()

admin_manager = Admin()

class RegisterMixin(object):
    def register(self, name):
        def deco(func):
            self.methods[name] = func
            return func
        return deco

    def has_registered(self, name):
        return name in self.methods

    def summary(self, *args, **kwargs):
        return self.methods["summary"](*args, **kwargs)

    def list(self, *args, **kwargs):
        return self.methods["list"](*args, **kwargs)

    def add(self, *args, **kwargs):
        return self.methods["add"](*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.methods["delete"](*args, **kwargs)

    def edit(self, *args, **kwargs):
        return self.methods["edit"](*args, **kwargs)

class Manager(RegisterMixin):
    def __init__(self, blueprint):
        self.name = blueprint.name
        self.blueprint = blueprint
        self.methods = {}
        self.modules = []
        self.modmap = {}
        # add this object to the blueprint, which will then be easily
        # accessible after the base admin.setup_app(app) is called
        blueprint.admin_manager = self

    def add_module(self, module):
        self.modules.append(module)
        self.modmap[module.name] = module
        module.manager = self

class Module(RegisterMixin):
    def __init__(self, name):
        self.name = name
        self.methods = {}

