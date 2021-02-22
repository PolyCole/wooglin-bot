import json


def slack_handler(event, context):
    body = {
        "message": "Way to go Slack, we've got you loud and clear.",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
