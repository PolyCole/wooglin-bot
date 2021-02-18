import os
import logging
import urllib
import re
import sys

from urllib import request, parse

# Bot authorization token from slack.
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Sending our replies here.
SLACK_URL = "https://slack.com/api/chat.postMessage"

def lambda_handler(data, context):
    print("RECEIVED:")
    print(data)

    # Verifying that our requests are actually coming from slack.
    if "token" in data:
        if data['token'] != os.environ['SLACK_VERIFICATION_TOKEN']:
            print("VERIFICATION FOR SLACK FAILED.")
            print("Terminating....")
            sys.exit(1)

    global SLACK_CHANNEL

    # Handles initial challenge with Slack's verification.
    if "challenge" in data:
        return data["challenge"]

    # Getting the data of the event.
    slack_event = data['event']

    # Ignore other bot events.
    if "bot_id" in slack_event:
        logging.warning("Ignore bot event")
        return "200 OK"
    else:
        # Parses out garbage text if user @'s the bot'
        text = slack_event["text"].lower()

        # Getting ID of channel where message originated.
        SLACK_CHANNEL = slack_event["channel"]

        if 'channel_type' in slack_event and slack_event['channel_type'] == "im":
            sendmessage("hiya")
        else:
            if mentions_me(text):
                sendmessage("hullo")
        return "200 OK"


def mentions_me(text):
    return text.find(os.environ['MY_ID']) != -1


def strip_text(text):
    # Pulling the nasty @tag out of the message.
    text = re.sub('<@.........>', "Wooglin,", text).strip()
    print("Text after @ removal: " + text)
    return text


def process_message_helper(text, slack_event):
    try:
        # Some classics.
        if text == "Wooglin " + os.environ['SECRET_PROMPT']:
            sendmessage(os.environ['SECRET_RESPONSE'])
        elif text == "Wooglin, play funkytown":
            sendmessage("https://www.youtube.com/watch?v=s36eQwgPNSE")
        # Not a given response, let's send the message to NLP.
        else:
            process_message(slack_event)
    except Exception as e:
        sendmessage("I've encountered an error: " + str(e))


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
