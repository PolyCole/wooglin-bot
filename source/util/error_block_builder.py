from .base_block_element_factory import *
from source.GreetUser import *


def get_nlu_error_block(response):
    blocks = [{
        get_markdown_block(":red_circle: :brain: Wooglin-NLU Error :brain: :red_circle:"),
        get_divider(),
        get_text_fields_block(response)
    }]

    return blocks


def get_nlu_confused_error_block(response):
    blocks = [{
        get_markdown_block(":thinking_face: :brain: Wooglin-NLU Didn't Understand :brain: :question:"),
        get_divider(),
        get_text_fields_block(response)
    }]

    return blocks


def notify_cole_error_block(slack_event, existing_error_blocks):
    pertinent_information_from_slack = {
        "message_text": slack_event['text'],
        "user": get_user_info(slack_event['user'])
    }

    blocks = [{
        get_markdown_block("Generic error output."),
        get_divider(),
        get_text_fields_block(pertinent_information_from_slack),
        get_divider(),
        existing_error_blocks
    }]

    return blocks
