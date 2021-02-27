from .custom_block_elements import *
from source.GreetUser import *
from slackblocks import SectionBlock, DividerBlock, HeaderBlock


def get_nlu_error_block(response):
    blocks = [
        HeaderBlock(":red_circle: :brain: Wooglin-NLU Error :brain: :red_circle:"),
        DividerBlock(),
        SectionBlock("*_NLU Response_*", fields=get_text_fields(response))
    ]

    return blocks


def get_nlu_confused_error_block(response):
    blocks = [
        HeaderBlock(":thinking_face: :brain: Wooglin-NLU Didn't Understand :brain: :question:"),
        DividerBlock(),
        SectionBlock("*_NLU Response_*", fields=get_text_fields(response))
    ]

    return blocks


def notify_cole_error_block(slack_event, existing_error_blocks):
    pertinent_information_from_slack = {
        "message_text": slack_event['text'],
        "user": get_user_info(slack_event['user'])
    }

    blocks = [
        HeaderBlock("Error Output"),
        DividerBlock(),
        SectionBlock("*_Message Details_*", fields=get_text_fields(pertinent_information_from_slack)),
        DividerBlock()
    ]

    for block in existing_error_blocks:
        blocks.append(block)

    return blocks
