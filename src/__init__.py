from src.dynamo_db_client import DynamoDBConnector
from src.slack_connector import sendMessageToSlack


def saveMessage(message):
    d = DynamoDBConnector()

    d.insertMessageRecord(message)

    sendMessageToSlack(
        f"Message received from {message['name']}: "
        f"\"{message['message']}\". "
        f"Reply back at {message['email']}"
    )
