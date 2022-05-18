import unittest
from app.main.views import new_comment
from app.models import Blog, Comment

class commentTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the post class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_comment = new_comment()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))