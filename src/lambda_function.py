from flask import Flask, request
from markupsafe import escape
import redis
import os
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Initialize Redis client with environment variables
redis_client = redis.Redis(
    host=os.getenv('MEMORYDB_HOST', 'localhost'),
    port=int(os.getenv('MEMORYDB_PORT', 6379)),
    password=os.getenv('MEMORYDB_PASSWORD', None),
    decode_responses=True  # This ensures we get strings back instead of bytes
)

KEY_NAME = 'dynamic_string'

def get_text_from_redis():
    try:
        text = redis_client.get(KEY_NAME)
        return text if text else 'dynamic string'
    except redis.RedisError as e:
        logger.error(f"Redis error: {str(e)}")
        return 'dynamic string'

def save_text_to_redis(text):
    try:
        redis_client.set(KEY_NAME, text)
    except redis.RedisError as e:
        logger.error(f"Redis error: {str(e)}")
        raise

@app.route('/text', methods=['GET'])
def get_text():
    # Get text from Redis
    text = get_text_from_redis()
    
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
    
    # Save text to Redis
    try:
        save_text_to_redis(text)
        return f'Text updated to: {text}', 200
    except redis.RedisError:
        return 'Error saving text', 500

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
