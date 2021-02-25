import logging
import re
import traceback
from source.util.error_block_builder import *
from source.util.informational_block_builder import *
from source.GreetUser import *

# Sending our replies here.
SLACK_URL = "https://slack.com/api/chat.postMessage"


def slack_handler(event, context):
    print("Event object received:")
    print(event)

    event_body = event['body']

    # Ensures we get the body of the request in a format we can work with.
    if type(event_body) is str:
        event_body = json.loads(event_body)

    global SLACK_CHANNEL

    # Verifying that our requests are actually coming from slack.
    if "token" in event_body:
        if event_body['token'] != os.environ["SLACK_VERIFICATION_TOKEN"]:
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
            return get_response_object(event, predefined_message_check(text, slack_event), statusCode=200)
        else:
            if mentions_me(text):
                return get_response_object(event, predefined_message_check(strip_text(text), slack_event), statusCode=200)

    return get_response_object(event)


# TODO: This whole flow needs refactoring.
def predefined_message_check(text, slack_event):
    # In all honesty, it's probably better to wake the NLU for this, but that's an expensive op and
    # I'm not sure I have the budget for it.
    # TODO: Revisit this section with the power of regex or something and clean it up.
    secret_prompt_message_variations = [
        os.environ['SECRET_PROMPT'],
        "wooglin " + os.environ['SECRET_PROMPT'],
        ", friendship"
    ]

    funkytown_message_variations = [
        'play funkytown',
        'play funky town',
        'wooglin, play funky town',
        'play funkytown wooglin',
        'play funky town wooglin'
    ]

    try:
        # Some classics.
        if text in secret_prompt_message_variations:
            print("Message contained secret prompt, returning secret response.")
            return sendmessage(os.environ['SECRET_RESPONSE'])
        elif text in funkytown_message_variations:
            print("Message requested funkytown.")
            return sendmessage("https://www.youtube.com/watch?v=s36eQwgPNSE")
        # Not a given response, let's send the message to NLP.
        else:
            return process_message(text, slack_event)
    except Exception as e:
        print("ERROR TRACEBACK:")
        print(traceback.print_exc())
        return sendmessage("I've encountered an error: " + str(e))


# Handles all messages that aren't predefined via wooglin-nlu.
def process_message(text, slack_event):
    nlu_response = get_nlu_response(text)
    print("nlu_response:")
    print(nlu_response)

    user = slack_event['user']

    if 'status' in nlu_response and nlu_response['status'] == 'failure':
        sendmessage(
            "I'm sorry, I seem to have encountered an error when raising the NLU.",
            get_nlu_error_block(nlu_response)
        )
        notify_cole("NLU Error encountered.", slack_event, get_nlu_error_block(nlu_response))
        return "NLU ERROR"

    # If the NLU was unable to accurately classify, let's tell the user we're confused.
    try:
        action = nlu_response['intent']['name']
        confidence = nlu_response['intent']['confidence']
    except KeyError:
        action = "confused"
        confidence = 0

    # Routing.
    if action == "confused" or confidence < 0.80 or action == "nlu_fallback":
        sendmessage("I'm sorry, I don't quite understand.", get_doc_block())
        notify_cole("NLU was confused on the following text. ", slack_event, get_nlu_confused_error_block(nlu_response))
        return "NLU Confused"
    elif action == "greet":
        return sendmessage(greet(user))
    # elif action == "database":
    #     DatabaseHandler.dbhandler(resp, user)
    # elif action == "sms":
    #     SMSHandler.smshandler(resp)
    else:
        sendmessage("Whoops! It looks like that feature hasn't been hooked up yet.")


def get_nlu_response(text):
    print("Sending text to the NLU engine...")
    return requests.post(os.environ['NLU_ADDRESS'], json.dumps({
        "text": text
    })).json()


# This process is significant. Due to the infrastructure serverless sets up,
# the response object NEEDS to be formatted in this exact manner.
# Failure to format responses in this manner will result in the response splatting against the outgoing side of the API.
def get_response_object(event, message="Slack message has been successfully handled.", statusCode=200):
    print("Message got: " + message)
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
    return text.find(os.environ['MY_ID']) != -1


# Removes the Bot's @ tag from the message for cleaner parsing.
def strip_text(text):
    # Pulling the nasty @tag out of the message.
    text = re.sub('<@.........>', "", text).strip()
    return text


# Sends a message in slack.
def sendmessage(message, blocks=None):
    print("Sending: " + message)

    msg_response = requests.post('https://slack.com/api/chat.postMessage', {
        'token': os.environ['BOT_TOKEN'],
        'channel': SLACK_CHANNEL,
        'text': message,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()

    print("RESPONSE FROM SLACK:")
    print(msg_response)

    return message


# Notify Cole in the event of an error.
def notify_cole(message, slack_event, error_blocks):
    blocks = notify_cole_error_block(slack_event, error_blocks)
    requests.post('https://slack.com/api/chat.postMessage', {
        'token': os.environ['BOT_TOKEN'],
        'channel': os.environ['COLE_DM'],
        'text': message,
        'blocks': json.dumps(blocks)
    }).json()


