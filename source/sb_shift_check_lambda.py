import requests
import json
import sys
import os

from slack_handler import sendmessage
from dateutil import parser

from source.util.sb_shift_block_builder import get_sb_shift_blocks


def sb_shift_handler(event, context):
    print(f"Periodic SB Shift Check Lambda received event: {event}")

    url = "https://wooglin-api.herokuapp.com/api/v1/next-sb-shift"
    headers = {"Authorization": f'Api-Key {os.environ["API_KEY"]}'}

    print("Starting request")
    response = requests.get(url, headers=headers)
    response_body = json.loads(response.content.decode("utf-8"))
    print("Request was: " + str(response_body))

    if 'no_shifts' in response_body:
        print("Check SB Shifts Operation completed successfully.\nThere are no shifts beginning in the next 15 minutes.")
        sys.exit(0)

    # This is me being doubly safe here. The API returns the shifts in a list,
    # which is guarding against the case wherein there are two shifts starting in the next
    # 15 minutes. Unlikely, but might as well make sure.
    for shift in response_body:
        title = shift["title"]
        date = shift["date"]

        time_start = parser.parse(shift["time_start"])
        time_end = parser.parse(shift["time_end"])

        sb_shift_message = "Looks like there's a SB Shift coming up, here are the details."
        sendmessage(sb_shift_message, get_sb_shift_blocks(title, date, time_start, time_end, shift['brothers']))


# TODO: This is duplicated from slack_handler. Need to break this out into a util or something.
# Sends a message in slack.
def sendmessage(message, blocks=None):
    print("Sending to SB Channel: " + message)

    msg_response = requests.post('https://slack.com/api/chat.postMessage', {
        'token': os.environ['BOT_TOKEN'],
        'channel': os.environ["COLE_DM"],
        'text': message,
        'blocks': str(blocks) if blocks else None
    }).json()

    print("RESPONSE FROM SLACK:")
    print(msg_response)

    return message