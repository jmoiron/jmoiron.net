#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""flatpages"""

from flask import *
from models import *
from models import blueprint as flatpage

from jmoiron.utils import Page, json_response, dumps

@flatpage.route("/<path:path>")
def index(path):
    path = "/%s" % path
    if path is "/favicon.ico":
        abort(404)
    page = list(Flatpage.find({"path":path}))
    if not page:
        abort(404)
    page = page[0]
    return render_template("flatpages/flatpage.html", **locals())


