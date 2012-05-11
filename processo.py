# -*- coding: utf-8 -*-

import functools

import webapp2
from google.appengine.api import users

# Login required decorator
def login_required(method, admin=False):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        user = users.get_current_user()
        if not user:
            if self.request.method == 'GET':
                self.redirect(users.create_login_url(self.request.uri))
                return
            self.error(403)
        elif admin and not users.is_current_user_admin():
            self.error(403)
        else:
            return method(self, *args, **kwargs)
    return wrapper

def admin_required(method):
    return login_required(method, admin=True)

class MainPage(webapp2.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello %s!' % user)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

