import json


def twilio_handler(event, context):
    body = {
        "message": "Roger roger Twilio, we read you loud and clear.",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
