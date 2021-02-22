import unittest
from source.twilio_handler import twilio_handler


class TestTwilioHandler(unittest.TestCase):

    """ test the handler code """
    def test_hello_world(self):
        event = {}
        context = {}

        resp = twilio_handler(event, context)
        self.assertEqual(resp["statusCode"], 200)


if __name__ == '__main__':
    unittest.main()