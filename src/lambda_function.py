from flask import Flask, request
from markupsafe import escape
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize DynamoDB client with environment variables
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv('LOCAL_AWS_ENDPOINT_URL', None),  # None will use default AWS endpoint
    aws_access_key_id=os.getenv('LOCAL_AWS_ACCESS_KEY_ID', None),  # None will use default credentials
    aws_secret_access_key=os.getenv('LOCAL_AWS_SECRET_ACCESS_KEY', None),  # None will use default credentials
    region_name='eu-west-2'
)

TABLE_NAME = os.getenv('DYNAMODB_TABLE', 'app-table')
table = dynamodb.Table(TABLE_NAME)

def get_text_from_dynamodb():
    try:
        response = table.get_item(Key={'id': 'main'})
        return response['Item']['text']
    except (ClientError, KeyError):
        # If the item doesn't exist, return default value
        return 'dynamic string'

def save_text_to_dynamodb(text):
    table.put_item(
        Item={
            'id': 'main',
            'text': text
        }
    )

@app.route('/text', methods=['GET'])
def get_text():
    # Get text from DynamoDB
    text = get_text_from_dynamodb()
    
    # Create HTML response with escaped text
    html_response = f'<h1>The saved string is {escape(text)}</h1>'
    
    return html_response, 200, {'Content-Type': 'text/html'}

@app.route('/text', methods=['PUT'])
def update_text():
    # Get text from request body
    text = request.get_data(as_text=True)
    if not text:
        return 'No text provided', 400
    
    # Check text length
    if len(text) > 256:
        return 'Text exceeds maximum length of 256 characters', 400
    
    # Save text to DynamoDB
    save_text_to_dynamodb(text)
    
    return f'Text updated to: {text}', 200

def lambda_handler(event, context):
    """AWS Lambda handler for API Gateway events"""
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        import awsgi
        return awsgi.response(app, event, context)
    except ImportError:
        # This will be used in local development
        return app(event, context)
    except Exception as e:
        logger.error(f"Error handling request: {str(e)}")
    return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
    } 
