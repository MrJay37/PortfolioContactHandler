from boto3 import resource
from datetime import datetime as dt
import os
from pytz import timezone
from uuid import uuid4


tz_name = os.getenv('TZ_NAME')


class TableNameNotProvided(Exception):
    def __init__(self):
        super().__init__(f'Table name not provided for DynamoDB connector')


class DynamoDBConnector:
    _TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
    
    def __init__(self):
        self._resource = resource('dynamodb')
        
        if self._TABLE_NAME is None:
            raise TableNameNotProvided()

        self._table = self._resource.Table(self._TABLE_NAME)

    def getTableInfo(self):
        return self._table.creation_date_time

    def getAllMessageRecords(self, **kwargs):
        return self._table.scan(**kwargs)

    def insertMessageRecord(self, record):
        item_count = self.getAllMessageRecords()['Count']

        self._table.put_item(
            Item={
                'messageId': str(uuid4()),
                'messageNo': item_count,
                **record,
                "responded_at": None,
                'created_at': str(dt.now(timezone(tz_name))),
                "is_spam": False
            }
        )

    def getMessageRecord(self, message_id, message_no):
        return self._table.get_item(
            Key={
                'messageId': message_id,
                'messageNo': message_no
            }
        )

    def deleteRecord(self, message_id, message_no):
        self._table.delete_item(
            Key={
                'messageId': message_id,
                'messageNo': message_no
            }
        )