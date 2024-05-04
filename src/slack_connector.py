import os
from requests import post

SLACK_CHANNEL_URL = os.getenv('SLACK_CHANNEL_URL')


class SlackNotificationFailed(Exception):
    def __init__(self, status_code, error_message):
        super().__init__(f"HTTP call to Slack channel failed [{status_code}]: {error_message}")


def sendMessageToSlack(message):
    res = post(
        url=SLACK_CHANNEL_URL,
        headers={
            'content-type': 'application/json'
        },
        json={
            "text": message
        }
    )

    if res.status_code == 200:
        return True

    raise SlackNotificationFailed(res.status_code, res.text)
