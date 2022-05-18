import unittest
from app.main.views import new_blog
from app.models import Blog

class BlogTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the post class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_blog = new_blog()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))