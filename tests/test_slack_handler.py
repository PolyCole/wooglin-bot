import unittest
from source.slack_handler import slack_handler


class TestSlackHandler(unittest.TestCase):

    """ test the handler code """
    def test_hello_world(self):
        event = {}
        context = {}

        resp = slack_handler(event, context)
        self.assertEqual(resp["statusCode"], 200)


if __name__ == '__main__':
    unittest.main()