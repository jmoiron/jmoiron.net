#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Faux models and miscellany to support simple admin CRUD."""

class Manager(object):
    def setup_app(self, app):
        self.config = app.config
        self.installed_apps = dict(app.blueprints)
        self.installed_apps.pop("admin", "")

admin_manager = Manager()

