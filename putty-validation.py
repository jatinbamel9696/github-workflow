import os
import sys
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
    This method fetches the existing tags and their values from the EC2 instance.
    '''
    try:
        instances = client.describe_instances(
            Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}]
        )
        
        # Check if any instances are found
        if not instances["Reservations"]:
            print(f"No instances found with the name: {instance_name}")
            return {}

        tag_set = instances["Reservations"][0]["Instances"][0].get("Tags", [])
        reserve_tags_for_ec2 = config['reserve_tags_for_ec2']
        
        # Create a dictionary of tags excluding reserved ones
        tags = {tag['Key']: tag['Value'] for tag in tag_set if tag['Key'] not in reserve_tags_for_ec2}
        
        print("Retrieved tags and values:", tags)
        return tags if tags else {}
    
    except ClientError as e:
        if "AccessDenied" in str(e):
            print("Access Denied: No instance found with this name in the selected account.")
            return {"Error": "Access Denied"}
        else:
            print("Error retrieving tags:", e)
            return {"Error": "Unable to retrieve tags."}

def main_connection():
    if len(sys.argv) != 2:
        print("Usage: python putty-validation.py <instance_name>")
        sys.exit(1)
    
    instance_name = sys.argv[1]
    client = boto3.client('ec2')
    
    tags = existing_tags(client, instance_name)
    
    # Only print the final tags to console
    print("Final Tags and Values:", tags)

    # Write tags as key-value pairs to $GITHUB_ENV if running in GitHub Actions
    if os.getenv('GITHUB_ENV'):
        with open(os.getenv('GITHUB_ENV'), 'a') as env_file:
            for key, value in tags.items():
                env_file.write(f"{key.upper()}={value}\n")

if __name__ == "__main__":
    main_connection()
