import boto3
import os

# Initialize boto3 clients
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localstack:4566',  # LocalStack endpoint
    aws_access_key_id='test',  # LocalStack credentials
    aws_secret_access_key='test',  # LocalStack credentials
    region_name='eu-west-2'
)

def create_dynamodb_table():
    try:
        dynamodb.create_table(
            TableName='app-table', # DynamoDB table name
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("DynamoDB table created successfully")
    except dynamodb.exceptions.ResourceInUseException:
        print("DynamoDB table already exists")

def main():
    print("Setting up LocalStack environment...")
    
    # Create DynamoDB table
    create_dynamodb_table()
    
    print("LocalStack setup completed!")

if __name__ == "__main__":
    main() 