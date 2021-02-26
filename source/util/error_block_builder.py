from .base_block_element_factory import *
from source.GreetUser import *


def get_nlu_error_block(response):
    blocks = {}
    blocks.update(get_markdown_block(":red_circle: :brain: Wooglin-NLU Error :brain: :red_circle:"))
    blocks.update(get_divider())
    blocks.update(get_text_fields_block(response))

    return [blocks]


def get_nlu_confused_error_block(response):
    blocks = {}
    blocks.update(get_markdown_block(":thinking_face: :brain: Wooglin-NLU Didn't Understand :brain: :question:"))
    blocks.update(get_divider())
    blocks.update(get_text_fields_block(response))

    return [blocks]


def notify_cole_error_block(slack_event, existing_error_blocks):
    pertinent_information_from_slack = {
        "message_text": slack_event['text'],
        "user": get_user_info(slack_event['user'])
    }

    blocks = {}
    blocks.update(get_markdown_block("Generic error output."))
    blocks.update(get_divider())
    blocks.update(get_text_fields_block(pertinent_information_from_slack))
    blocks.update(get_divider())
    blocks.update(existing_error_blocks[0])

    return [blocks]
