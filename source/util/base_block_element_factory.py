def get_markdown_block(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def get_divider():
    return {
               "type": "divider"
           }


def get_text_fields_block(object):
    base = {"type": "section"}
    fields = []

    for item in object.items():
        key, value = item
        current_field = {"type": "mrkdwn", "text": "*" + key + "*: " + str(value)}
        fields.append(current_field)

    base['fields'] = fields

    return base
