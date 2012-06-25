import google.appengine.tools # causes an exception in production, as desired
import unittest
import sys
import StringIO

from tests import *

import webapp2

class TestSuiteHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('%s\n Tests\n%s\n\n' % ('=' * 70, '=' * 70))
        modules = [sys.modules['tests.%s' % m] for m in dir(sys.modules['tests']) if m.startswith('test')]
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for module in modules:
            suite.addTest(loader.loadTestsFromModule(module))

        # Fake flush method called by TextTestRunner
        self.response.out.flush = lambda: None

        runner = unittest.TextTestRunner(self.response.out)
        runner.run(suite)

app = webapp2.WSGIApplication([('/test/?', TestSuiteHandler)], debug=True)

