"""
This module contains the repository for the DynamoDB table.
"""
import os
import boto3
from botocore.exceptions import ClientError


class Repository:
    """
    Repository for the DynamoDB table.
    """
    def __init__(self):
        """
        Initialize the repository.
        """
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=os.getenv('LOCAL_AWS_ENDPOINT_URL', None),
            aws_access_key_id=os.getenv('LOCAL_AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=os.getenv('LOCAL_AWS_SECRET_ACCESS_KEY', None),
            region_name='eu-west-2'
        )
        table_name = os.getenv('DYNAMODB_TABLE', 'app-table')
        table = dynamodb.Table(table_name)
        self.table = table

    def get_text_from_dynamodb(self):
        """
        Get text from DynamoDB.
        """
        try:
            response = self.table.get_item(Key={'id': 'main'})
            return response['Item']['text']
        except (ClientError, KeyError):
            return 'dynamic string'

    def save_text_to_dynamodb(self, text):
        """
        Save text to DynamoDB.
        """
        self.table.put_item(
            Item={
                'id': 'main',
                'text': text
            }
        )
