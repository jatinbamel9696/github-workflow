import boto3
import os
import sys
from datetime import datetime

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Adjust region if needed

def update_status_to_failed(request_id):
    # Get table name from environment variable
    table_name = os.getenv('TABLE_NAME')
    if not table_name:
        print("Environment variable TABLE_NAME is not set.")
        sys.exit(1)

    table = dynamodb.Table(table_name)

    try:
        # Update the status and timestamp
        response = table.update_item(
            Key={'Request-Id': request_id},  # Primary Key
            UpdateExpression="SET #status = :status, #update_timestamp = :update_timestamp",
            ExpressionAttributeNames={
                "#status": "Status",
                "#update_timestamp": "update_timestamp"
            },
            ExpressionAttributeValues={
                ":status": "Failed",  # Update status to Failed
                ":update_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
            },
            ReturnValues="UPDATED_NEW"  # Return updated attributes
        )
        print(f"Successfully updated Request ID {request_id}: {response['Attributes']}")
    except Exception as e:
        print(f"Failed to update status: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_status_failed.py <request_id>")
        sys.exit(1)

    request_id = sys.argv[1]
    update_status_to_failed(request_id)
