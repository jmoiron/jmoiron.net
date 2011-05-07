#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""blog views."""

from flask import *
from models import *
from utils import Page, json_response, dumps

comments = Module(__name__, 'comments')

per_page = 20

