import boto3
import os
import sys
from botocore.exceptions import ClientError
from datetime import datetime

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Adjust region as needed

def insert_request_id(request_id):
    table_name = os.getenv('TABLE_NAME')  # Read table name from environment variable
    if not table_name:
        print("Environment variable TABLE_NAME is not set.")
        sys.exit(1)
    
    table = dynamodb.Table(table_name)

    # Define the item to insert
    item = {
        'Request-Id': request_id,                # Primary Key
        'Instance-Name': 'NA',                        # Replace with actual hostname if available
        'Status': 'Initiated',                   # Initial status
        'Attributes': 'NA',                      # Placeholder for attributes, replace if needed
        'create-timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Current time as creation date
        'update_timestamp' : 'NA'                                 # Placeholder for update time
    }

    try:
        # Insert item using put_item
        response = table.put_item(Item=item)
        print(f"Request ID inserted successfully: {response}")
    except ClientError as e:
        print(f"Failed to insert request ID: {e.response['Error']['Message']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dynamodb_insert_request_id.py <request_id>")
        sys.exit(1)

    request_id = sys.argv[1]
    insert_request_id(request_id)