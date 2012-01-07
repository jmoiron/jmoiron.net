#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""jmoiron.net main application"""

import os
import re
import time
import argot

from flask import *

from micromongo import connect, current
from jmoiron.utils import import_module

from jmoiron.admin.models import admin_manager
from jmoiron.auth.models import login_manager

app = Flask(__name__)

def register_blueprint(package):
    """A custom function which registers a blueprint and loads its views and
    admin modules so that all of the routes get hooked up at the right time."""
    models = import_module("%s.models" % package)
    if not models:
        raise Exception("Could not import models from package %s" % package)
    import_module("%s.views" % package)
    import_module("%s.admin" % package)
    if hasattr(models, "url_prefix"):
        app.register_blueprint(models.blueprint, url_prefix=models.url_prefix)
    else:
        app.register_blueprint(models.blueprint)


runlevel = os.environ.get("JMOIRON_RUNLEVEL", "Development")
app.config.from_object("config.%sConfig" % runlevel)

connect(app.config["DATABASE_URI"])
dbname = app.config["DATABASE_NAME"]

blueprints = (
    "jmoiron.blog",
    "jmoiron.stream",
    "jmoiron.comments",
    "jmoiron.auth",
    "jmoiron.admin",
)

for blueprint in blueprints:
    try:
        register_blueprint(blueprint)
    except:
        import traceback
        print "Error registering %s" % blueprint
        traceback.print_exc()

login_manager.setup_app(app)


# -- request setup/shutdown --

@app.before_request
def before_request():
    g.db = current()[dbname]
    g.section = filter(None, request.path.split("/"))
    g.section = g.section[0] if g.section else "index"

@app.after_request
def after_request(response):
    return response

# -- leftover urls --

@app.route("/")
def index():
    from stream.views import index
    return index()

@app.errorhandler(404)
def page_not_found(e):
    return "HTTP 404: page not found", 404

# flatpages have to come after this I guess..
register_blueprint("jmoiron.flatpages")

# register everything with the admin manager
admin_manager.setup_app(app)

# -- jinja2 filters --

@app.template_filter("pdt")
def pretty_datetime(dt):
    """Show date in a pretty way, similar to new default datetime in django."""
    from utils import utc_to_timezone
    dt = utc_to_timezone(dt, "US/Eastern")
    return time.strftime("%B %d, %Y, %I:%M %p", dt.timetuple())\
            .replace("AM", "a.m.")\
            .replace("PM", "p.m.")

@app.template_filter("argot")
def argot_filter(string):
    return argot.render(str(string))

if __name__ != "__main__":
    db = current()[dbname]

