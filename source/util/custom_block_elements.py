from slackblocks import Text

# Takes in a map, produces a list of text fields that have the key name in bold followed by the value.
def get_text_fields(data):
    fields = []

    for item in data.items():
        key, value = item
        current_field = Text("*" + key + "*: " + str(value))
        fields.append(current_field)

    return fields
