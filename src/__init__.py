from src.dynamo_db_client import DynamoDBConnector
from src.slack_connector import sendMessageToSlack
from uuid import UUID
import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class ValidationError(Exception):
    def __init__(self, key, value):
        super().__init__(f"Invalid '{key}' value for message: {value}")


def validateUUID(uuid_string):
    try:
        UUID(uuid_string, version=4)

    except (ValueError, TypeError):
        return False

    return True


def validateEmail(email):
    return re.fullmatch(EMAIL_REGEX, email)


def validateString(value):
    return isinstance(value, str)


VALIDATORS = {
    'appId': lambda x: validateUUID(x),
    'name': lambda x: validateString(x),
    'email': lambda x: validateEmail(x),
    'message': lambda x: validateString(x)
}


def saveMessage(message):
    d = DynamoDBConnector()

    message_obj = {}

    for key in ['appId', 'name', 'email', 'message']:
        try:
            value = message[key]

        except KeyError:
            raise ValidationError(key, None)

        validated = VALIDATORS[key](value)

        if not validated:
            raise ValidationError(key, value)

        message_obj[key] = value

    d.insertMessageRecord(message)

    sendMessageToSlack(
        f"Message received from {message['name']}: "
        f"\"{message['message']}\". "
        f"Reply back at {message['email']}"
    )
