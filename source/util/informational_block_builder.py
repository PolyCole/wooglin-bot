def get_doc_block():
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Click on the button to see my documentation."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Read My Documentation :book:",
                    "emoji": True
                },
                "value": "click_for_docs",
                "url": "https://github.com/WooglinAlphaZeta/wooglin-bot",
                "action_id": "button-action"
            }
        }
    ]
