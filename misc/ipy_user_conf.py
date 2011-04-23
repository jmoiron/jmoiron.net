from run import app, db, before_request
# set up a flask environment
ctx = app.test_request_context('/')
ctx.push()
before_request()
# import stuff i want
from utils import *
from stream.models import *
from blog.models import *
