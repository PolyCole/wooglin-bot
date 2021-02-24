import unittest
from testing_utilities import populate_environment
from source.slack_handler import *


class TestSlackHandler(unittest.TestCase):
    """ test the handler code """
    def setUp(self):
        try:
            test = os.environ['BOT_TOKEN']
        except KeyError:
            populate_environment()

    def test_mentions_me_returns_proper_response(self):
        self.assertEqual(mentions_me("Hello world"), False)
        self.assertEqual(mentions_me("Good morning, " + os.environ['MY_ID']), True)


if __name__ == '__main__':
    unittest.main()