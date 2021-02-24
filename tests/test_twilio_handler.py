import unittest
from testing_utilities import populate_environment
from source.slack_handler import *


class TestTwilioHandler(unittest.TestCase):
    """ test the handler code """
    def setUp(self):
        try:
            test = os.environ['BOT_TOKEN']
        except KeyError:
            populate_environment()


if __name__ == '__main__':
    unittest.main()