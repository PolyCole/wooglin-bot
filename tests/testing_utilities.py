import json
import os
import sys
from pathlib import Path


def populate_environment():
    base_dir = Path(__file__).resolve().parent.parent
    secrets_path = os.path.join(base_dir, 'secrets.json')

    secrets = None
    if os.path.isfile(secrets_path):
        print("Found local secrets file, reading secrets...")
        with open(secrets_path) as f:
            secrets = json.load(f)
    else:
        print("Secrets file not found, this is critical for testing. Aborting...")
        sys.exit(1)

    for item in secrets.items():
        key, value = item
        os.environ[key] = value

    print("Successfully loaded environment variables from secrets.json.")


def get_request_object():
    return {
        'resource': '/slackhook',
        'httpMethod': 'POST',
        'headers': {},
        'isBase64Encoded': False
    }
