#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""configuration for jmoiron.net"""

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "jmoiron"
    SECRET_KEY = '\x10t\x98\xaeR:0\xc2\xea\x8frl b=\xde'
    USE_LESS = True

class DevelopmentConfig(Config):
    DEBUG = True
    OFFLINE_MODE = True
    #USE_LESS = False

class ProductionConfig(Config):
    pass

