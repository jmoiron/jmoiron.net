#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""blog views."""

from flask import *
from models import *

from jmoiron.utils import Page, json_response, dumps

per_page = 20

