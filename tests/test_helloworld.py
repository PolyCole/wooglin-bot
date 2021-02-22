import unittest
from source.handler import wooglin_handler

class TestHelloWorld(unittest.TestCase):

    """ test the handler code """
    def test_hello_world(self):
        event = {}
        context = {}

        resp = wooglin_handler(event, context)
        self.assertEqual(resp["statusCode"], 200)


if __name__ == '__main__':
    unittest.main()