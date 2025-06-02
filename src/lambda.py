"""
This module contains the Lambda function for the API Gateway.
"""
import json
import logging
import awsgi
from app import app


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """AWS Lambda handler for API Gateway events"""
    logger.info("Received event: %s", json.dumps(event))

    try:
        return awsgi.response(app, event, context)
    except ImportError:
        return app(event, context)
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        logger.error("Error handling request: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
