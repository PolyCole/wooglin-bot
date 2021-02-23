import json
import os
import sys
import logging
import re
import urllib
import json

# Bot authorization token from slack.
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Sending our replies here.
SLACK_URL = "https://slack.com/api/chat.postMessage"


def slack_handler(event, context):
    print("Event object received:")
    print(event)

    event = event['body']

    if type(event) is str:
        event = json.loads(event)

    global SLACK_CHANNEL

    # Verifying that our requests are actually coming from slack.
    if "token" in event:
        if event['token'] != os.environ["SLACK_VERIFICATION_TOKEN"]:
            print("VERIFICATION FOR SLACK FAILED.")
            print("This request didn't come from slack, telling sender to kindly go away.")
            return {
                "message": "Events originating outside of slack are not allowed.",
                "statusCode": 401
            }
    else:
        return {
            "message": "Requests must contain a valid verification token.",
            "statusCode": 400
        }

    # Handles initial challenge with Slack's verification.
    if "challenge" in event:
        return event["challenge"]

    # Getting the slack data of the event.
    slack_event = event['event']

    # Ignore other bot events.
    if "bot_id" in slack_event:
        logging.warning("Ignore bot event")
        return get_response_object(event, "Message is already being handled.", statusCode=200)
    else:
        # Parses out garbage text if user @'s the bot'
        text = slack_event["text"].lower()

        # Getting ID of channel where message originated.
        SLACK_CHANNEL = slack_event["channel"]

        # If we're dealing with a DM channel, let's respond. Otherwise, let's ensure we're being @'ed.
        if 'channel_type' in slack_event and slack_event['channel_type'] == "im":
            predefined_message_check(text, slack_event)
        else:
            if mentions_me(text):
                predefined_message_check(strip_text(text), slack_event)

    return get_response_object(event)


def predefined_message_check(text, slack_event):
    try:
        # Some classics.
        if text == "Wooglin " + os.environ['SECRET_PROMPT']:
            sendmessage(os.environ['SECRET_RESPONSE'])
        elif text == "Wooglin, play funkytown" or text == "Wooglin play funkytown":
            sendmessage("https://www.youtube.com/watch?v=s36eQwgPNSE")
        # Not a given response, let's send the message to NLP.
        else:
            print("Un-implemented.")
            # This gets more complicated.
            # process_message(slack_event)
    except Exception as e:
        sendmessage("I've encountered an error: " + str(e))


def get_response_object(event, message="Slack message has been successfully handled.", statusCode=200):
    body = {
        "message": message,
        "input": event
    }

    response = {
        "statusCode": statusCode,
        "body": json.dumps(body)
    }

    return response


def mentions_me(text):
    return text.find(os.environ['MY_ID']) != -1


def strip_text(text):
    # Pulling the nasty @tag out of the message.
    text = re.sub('<@.........>', "Wooglin,", text).strip()
    return text


# Sends a message in slack.
def sendmessage(message):
    print("Sending: " + message)

    # Crafting our response.
    data = urllib.parse.urlencode(
        (
            ("token", BOT_TOKEN),
            ("channel", SLACK_CHANNEL),
            ("text", message)
        )
    )

    # Encoding
    data = data.encode("ascii")

    # Creating HTTP POST request.
    requestHTTP = urllib.request.Request(SLACK_URL, data=data, method="POST")

    # Adding header.
    requestHTTP.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded"
    )

    # Request away!
    urllib.request.urlopen(requestHTTP).read()
    return "200 OK"
