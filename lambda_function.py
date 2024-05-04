import json
import logging
from src import *


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    headers = event['headers']
    request_context = event['requestContext']
    http_info = request_context['http']
    message = json.loads(event['body'])
    raw_path = event['rawPath']

    if raw_path == '/message' and http_info['method'].upper() == 'POST':
        logging.info(
            f"Message received from {headers['x-forwarded-for']};"
            f"user agent {headers['user-agent']}"
        )

        saveMessage(message)

        return {
            'statusCode': 200,
            'body': 'Message received'
        }

    return {
        'statusCode': 404,
        'body': "Not Found"
    }
