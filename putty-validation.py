import os
import sys
import json
import boto3
import yaml
from botocore.exceptions import ClientError

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
common_folder = os.path.join(script_dir, 'common')

try:
    with open(os.path.join(common_folder, 'config.yml'), 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    print("Configuration file 'config.yml' not found in 'common' folder.")
    sys.exit(1)

def existing_tags(client, instance_name):
    '''
    This method fetches the existing tag from the EC2 instance
    '''
    try:
        instances = client.describe_instances(
            Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}]
        )
        # if not instances["Reservations"]:
        #     print(f"No instances found with the name: {instance_name}")
        #     return []
        tag_set = instances["Reservations"][0]["Instances"][0]["Tags"]
        #tag_set = instances["Reservations"][0]["Instances"][0].get("Tags", [])
        reserve_tags_for_ec2 = config.get('reserve_tags_for_ec2', [])
        
        tags = [tag['Key'] for tag in tag_set if tag['Key'] not in reserve_tags_for_ec2]
        
        print("Retrieved tags: ", tags)
        return tags if tags else []
    
    except ClientError as e:
        if "AccessDenied" in str(e):
            print("Access Denied: No instance found with this name in the selected account.")
            return ["Access Denied: No instance found with this name in the selected account."]
        else:
            print("Error retrieving tags:", e)
            return ["Error: Unable to retrieve tags."]

def main_connection():
    if len(sys.argv) != 2:
        print("Usage: python aws_tags.py <instance_name>")
        sys.exit(1)
    
    instance_name = sys.argv[1]
    client = boto3.client('ec2')
    
    tags = existing_tags(client, instance_name)
    print("Final Tags:", tags)
    print(type(tags))

if __name__ == "__main__":
    main_connection()