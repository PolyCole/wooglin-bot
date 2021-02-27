from slackblocks import SectionBlock, Button


def get_doc_block():
    button = Button(
        "Read My Documentation :book:",
        action_id="doc_link",
        url="https://github.com/WooglinAlphaZeta/wooglin-bot"
    )

    blocks = [
        SectionBlock("I'm sorry, I don't fully understand. Click to see my documentation.", accessory=button),

    ]

    return blocks
