from main import app
from utils import TestCase

class TestUrlStatus(TestCase):
    def test_root(self):
        ''' Tests for 200 status code on index. '''
        response = app.get_response('/')
        self.assertEqual(response.status_int, 200)

    def test_sign(self):
        ''' Tests create a greeting. It should return a 302 (redirect) status. '''
        response = app.get_response('/sign', POST={'content': 'The content'})
        self.assertEqual(response.status_int, 302)


