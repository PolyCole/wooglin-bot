import unittest
from testing_utilities import populate_environment, get_request_object
from source.slack_handler import *


class TestSlackHandler(unittest.TestCase):
    """ test the handler code """
    def setUp(self):
        try:
            test = os.environ['BOT_TOKEN']
        except KeyError:
            populate_environment()

    def test_slack_handler_requires_valid_token(self):
        # First, trying without a token all together.
        request = get_request_object()
        request['body'] = '{"hello": "world"}'
        response = slack_handler(request, {})
        self.assertEqual(response['statusCode'], 400)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['message'], "Requests must contain a valid verification token.")

        # Second, trying with an invalid token
        request['body'] = '{"hello": "world", "token": "hElLo Im ToTaLlY wOoGlIn"}'
        response = slack_handler(request, {})
        self.assertEqual(response['statusCode'], 401)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['message'], "Events originating outside of slack are not allowed.")

    def test_slack_challenge_is_handled(self):
        request = get_request_object()
        request_body = {
            "challenge": "Hello, world",
            "token": os.environ['SLACK_VERIFICATION_TOKEN']
        }
        request['body'] = json.dumps(request_body)
        response = slack_handler(request, {})
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['challenge'], 'Hello, world')

    def test_bot_events_are_ignored(self):
        request = get_request_object()
        request_body = {
            "token": os.environ['SLACK_VERIFICATION_TOKEN'],
            "event": {
                "bot_id": "bEeP bOoP"
            }
        }
        request['body'] = json.dumps(request_body)
        response = slack_handler(request, {})
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['message'], "Message is being ignored since it's a bot event.")

    def test_predefined_messages_group_channel(self):
        request = get_request_object()
        request_body = {
            "token": os.environ['SLACK_VERIFICATION_TOKEN'],
            "event": {
                "text": os.environ['MY_ID'] + " play funkytown",
                "channel": os.environ['DEFAULT_CHANNEL']
            }
        }
        request['body'] = json.dumps(request_body)
        response = slack_handler(request, {})

        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['message'], "https://www.youtube.com/watch?v=s36eQwgPNSE")

        request_body = {
            "token": os.environ['SLACK_VERIFICATION_TOKEN'],
            "event": {
                "text": os.environ['MY_ID'] + " " + os.environ['SECRET_PROMPT'],
                "channel": os.environ['DEFAULT_CHANNEL']
            }
        }
        request['body'] = json.dumps(request_body)
        response = slack_handler(request, {})
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])
        self.assertEqual(response_body['message'], os.environ['SECRET_RESPONSE'])

    def test_mentions_me_returns_proper_response(self):
        self.assertEqual(mentions_me("Hello world"), False)
        self.assertEqual(mentions_me("Good morning, " + os.environ['MY_ID']), True)

    def test_strip_text(self):
        text = "Good morning, " + os.environ['MY_ID']
        self.assertEqual(strip_text(text), "Good morning,")

        text = "Hello world"
        self.assertEqual(strip_text(text), text)


if __name__ == '__main__':
    unittest.main()