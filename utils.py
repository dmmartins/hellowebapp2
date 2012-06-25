'''
Google Appengine utils.
Everything I need to create a simple app using webapp2 framework.
'''

import os
import unittest

import webapp2
import jinja2
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import users
from google.appengine.ext import testbed

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_DIR))

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


class BaseHandler(webapp2.RequestHandler):
    ''' A basic handler that provides common methods. '''
    def render(self, template_name, dictionary={}):
        template = jinja2_env.get_template(template_name)
        template_values = self._context

        # Dictionary overwrites values on context
        template_values.update(dictionary)
        self.response.out.write(template.render(template_values))

    @property
    def _context(self):
        ''' Default values for context. '''
        if users.get_current_user():
            auth_url = users.create_logout_url(self.request.uri)
            auth_text = u'Logout'
        else:
            auth_url = users.create_login_url(self.request.uri)
            auth_text = u'Login'

        return {'auth_url': auth_url, 'auth_text': auth_text}

class TestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

