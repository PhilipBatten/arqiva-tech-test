"""
This module contains the Flask application.
"""
import logging
from flask import Flask, request
from markupsafe import escape
from dotenv import load_dotenv
from repository import Repository


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize repository
repository = Repository()


@app.route('/text', methods=['GET'])
def get_text():
    """
    Get text from repository and return it as an HTML response.
    """
    # Get text from DynamoDB
    text = repository.get_text_from_dynamodb()
    # Create HTML response with escaped text
    html_response = f'<h1>The saved string is {escape(text)}</h1>'
    return html_response, 200, {'Content-Type': 'text/html'}


@app.route('/text', methods=['PUT'])
def update_text():
    """
    Update text via repository.
    """
    # Get text from request body
    text = request.get_data(as_text=True)
    if not text:
        return 'No text provided', 400
    # Check text length
    if len(text) > 256:
        return 'Text exceeds maximum length of 256 characters', 400
    # Save text to DynamoDB
    repository.save_text_to_dynamodb(text)
    return f'Text updated to: {text}', 200
