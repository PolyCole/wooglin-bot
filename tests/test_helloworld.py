import unittest
from handler import hello

class TestHelloWorld(unittest.TestCase):

    """ test the handler code """
    def test_hello_world(self):
        event = {}
        context = {}

        resp = hello(event, context)
        self.assertEqual(resp["statusCode"], 200)


if __name__ == '__main__':
    unittest.main()