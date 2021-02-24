import os
import logging
import re
import requests
import json

# Bot authorization token from slack.
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Sending our replies here.
SLACK_URL = "https://slack.com/api/chat.postMessage"


def slack_handler(event, context):
    print("Event object received:")
    print(event)

    event_body = event['body']

    # Ensures we get the body of the request in a format we can work with.
    if type(event_body) is str:
        event_body = json.loads(event)

    global SLACK_CHANNEL

    # Verifying that our requests are actually coming from slack.
    if "token" in event_body:
        token = os.environ["SLACK_VERIFICATION_TOKEN"].split(",")
        if event_body['token'] != token[0] and event_body['token'] != token[1]:
            print("VERIFICATION FOR SLACK FAILED.")
            print("This request didn't come from slack, telling sender to kindly go away.")
            return get_response_object(event, "Events originating outside of slack are not allowed.", 401)
        else:
            print("Token verification has succeeded. The request came from slack.")
    else:
        return get_response_object(event, "Requests must contain a valid verification token.", 400)

    # Handles initial challenge with Slack's verification.
    if "challenge" in event_body:
        response = get_response_object(event, "Challenge received, returning...", 200)
        response["challenge"] = event_body["challenge"]
        print("Responding to slack challenge with: " + json.dumps(response))
        return response

    # Getting the slack data of the event.
    slack_event = event_body['event']

    # Ignore other bot events.
    if "bot_id" in slack_event:
        logging.debug("Bot id detected, subsequently ignored. ")
        return get_response_object(event, "Message is being ignored since it's a bot event.", statusCode=200)
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
    # In all honesty, it's probably better to wake the NLU for this, but that's an expensive op and
    # I'm not sure I have the budget for it.
    # TODO: Revisit this section with the power of regex or something and clean it up.
    secret_prompt_message_variations = [
        os.environ['SECRET_PROMPT'],
        "Wooglin, " + os.environ['SECRET_PROMPT'],
        "Wooglin " + os.environ['SECRET_PROMPT']
    ]

    funkytown_message_variations = [
        'Wooglin, play funkytown',
        'Wooglin play funkytown',
        'play funkytown',
        'play funky town',
        'Wooglin, play funky town'
    ]

    try:
        # Some classics.
        if text in secret_prompt_message_variations:
            print("Message contained secret prompt, returning secret response.")
            sendmessage(os.environ['SECRET_RESPONSE'])
        elif text in funkytown_message_variations:
            print("Message requested funkytown.")
            sendmessage("https://www.youtube.com/watch?v=s36eQwgPNSE")
        # Not a given response, let's send the message to NLP.
        else:
            print("Un-implemented.")
            # This gets more complicated.
            # process_message(slack_event)
    except Exception as e:
        sendmessage("I've encountered an error: " + str(e))


# This process is significant. Due to the infrastructure serverless sets up,
# the response object NEEDS to be formatted in this exact manner.
# Failure to format responses in this manner will result in the response splatting against the outgoing side of the API.
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


# Checks to see if the bot's @ tag is included in the message.
def mentions_me(text):
    identities = os.environ['MY_ID'].split(",")

    mentioned = 0
    for x in range(0, len(identities)):
        if text.find(identities[0] != -1):
            mentioned += 1

    # TODO Write extra logic here to determine what to do if an identity collision occurs.
    # Back of the napkin math suggests this is EXCEEDINGLY unlikely ~ hypothetically 1/36^9
    if mentioned > 1:
        sendmessage("Identity collision.")
        raise Exception("We have a collision with identities. Aborting. Also, buy a lottery ticket.")

    return mentioned == 1


# Removes the Bot's @ tag from the message for cleaner parsing.
def strip_text(text):
    # Pulling the nasty @tag out of the message.
    text = re.sub('<@.........>', "Wooglin,", text).strip()
    return text


# Sends a message in slack.
def sendmessage(message, blocks=None):
    print("Sending: " + message)

    requests.post('https://slack.com/api/chat.postMessage', {
        'token': os.environ['BOT_TOKEN'],
        'channel': SLACK_CHANNEL,
        'text': message,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()

    return 200
