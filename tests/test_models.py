from main import Greeting
from utils import TestCase

class TestModel(TestCase):
    def test_create(self):
        greeting = Greeting()
        greeting.content = 'Test greeting'
        greeting.put()

        query = Greeting.query().fetch(10)
        self.assertEqual(len(query), 1)
        self.assertEqual(query[0].content, 'Test greeting')

