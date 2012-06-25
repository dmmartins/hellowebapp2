# -*- coding: utf-8 -*-
import os
import functools

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from utils import BaseHandler

DEBUG = os.environ.get("SERVER_SOFTWARE", "").startswith("Development/")


class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(BaseHandler):
    def get(self):
        grettings = Greeting.query()
        self.render('index.html', {'greetings': grettings})


class GreetingHandler(BaseHandler):
    def post(self):
        greeting = Greeting()
        greeting.author = users.get_current_user()
        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', GreetingHandler),], debug=DEBUG)

