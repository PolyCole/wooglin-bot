import json
import os
import random
import requests


# Method greets the user using their name.
def greet(user_id):
    name = get_user_info(user_id)

    # Greetings to select from.
    greetings = ["Hi", "Hello", "Hey", "What\'s up",
               "Waddup", "How are we", "Howdy", "Yo",
               "Good day", "What's poppin", "What\'s crackalakin'",
               "Hi there", "Hello there", "Hey there", "Howdy there",
               "Hello there"]

    greeting_num = random.randint(0, len(greetings) - 1)
    return greetings[greeting_num] + " " + name + "."


# Getting the user information from the slack API.
def get_user_info(user_id):
    user_data = {"user": {"real_name": "Error McErrorFace"}}

    try:
        slack_users_url = "https://slack.com/api/users.info"

        body = {
            "token": os.environ['BOT_TOKEN'],
            "user": user_id,
            "include_locale": "false"
        }

        user_data = requests.post(slack_users_url, body).json()
        print("Slack user api returned: " + user_data)

        if 'ok' in user_data and user_data['ok'] is False:
            print("Error encountered when trying to interact with Users API: " + user_data['error'])
            raise Exception("I've encountered an error: " + user_data['error'])

    except Exception as e:
        print(e)

    # Giving back the real name of the user.
    return user_data["user"]["real_name"]
