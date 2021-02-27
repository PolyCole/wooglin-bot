from slackblocks import Text


def get_text_fields(data):
    fields = []

    for item in data.items():
        key, value = item
        current_field = Text("*" + key + "*: " + str(value))
        fields.append(current_field)

    return fields
