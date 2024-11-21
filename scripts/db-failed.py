import boto3
import os
import sys
from botocore.exceptions import ClientError
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize the DynamoDB client
region = os.getenv('AWS_REGION', 'us-east-1')  # Adjust region if needed
dynamodb = boto3.resource('dynamodb', region_name=region)

def update_status_to_failed(request_id):
    table_name = os.getenv('TABLE_NAME')  # Read table name from environment variable
    if not table_name:
        logging.error("Environment variable TABLE_NAME is not set.")
        sys.exit(1)
    
    table = dynamodb.Table(table_name)

    # Define update expressions
    update_expression = "SET #status = :status, #update_timestamp = :update_timestamp"
    expression_attribute_names = {
        "#status": "Status",
        "#update_timestamp": "update_timestamp",
        "#request_id": "Request-Id"  # Escape 'Request-Id'
    }
    expression_attribute_values = {
        ":status": "Failed",  # Set status to 'Failed'
        ":update_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
    }

    try:
        # Perform the update
        response = table.update_item(
            Key={"#request_id": request_id},  # Use escaped key name
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression="attribute_exists(#request_id)",  # Use escaped attribute name
            ReturnValues="UPDATED_NEW"
        )
        logging.info(f"Successfully updated Request ID {request_id} to 'Failed'. Updated attributes: {response['Attributes']}")
        return response['Attributes']
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            logging.error(f"Request ID {request_id} does not exist in the table.")
        else:
            logging.error(f"Failed to update status: {e.response['Error']['Message']}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python db-failed.py <request_id>")
        sys.exit(1)

    request_id = sys.argv[1]
    update_status_to_failed(request_id)
