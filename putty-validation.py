import os
import sys
import json
import boto3
import yaml

script_dir = os.path.dirname(os.path.abspath(__file__))
common_folder = os.path.join(script_dir, 'common')

# Load the YAML file
with open(os.path.join(common_folder, 'config.yml'), 'r') as file:
    config = yaml.safe_load(file)

def existing_tags(client, instance_name):
    '''
    This method fetches the existing tag from the ec2 instance
    '''
    global config
    try:
        instances = client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        instance_name,
                    ]
                },
            ])
        tag_set = instances["Reservations"][0]["Instances"][0]["Tags"]
        reserve_tags_for_ec2 = config['reserve_tags_for_ec2']
        keyset = []
        for tag in tag_set:
            keyset.append(tag['Key'])
        
        print(keyset)
        tags = [i for i in keyset if i not in reserve_tags_for_ec2]

        
        print("Exit from Existing Tags...!") 
        if len(tags) > 0:
            return tags
        else:
            return []
        
    except Exception as e:
        print("EXCEPTION : existing_tags>>>>>>", str(e))
        tag_set = ' '
        ClientError = "An error occurred (AccessDenied)"

        if ClientError in str(e):
            print("EXCEPTION: No Instance found with this name in the selected account")
            return["EXCEPTION: No Instance found with this name in the selected account"]
        else:
            print("EXCEPTION in Existing Tags : ", str(e))
            return["EXCEPTION: No Instance found with this name in the selected account"]

def main_connection():
    try:
        # Accept Instance from cmd
        if len(sys.argv) != 2:
            print("Usage: python aws_tags.py <instance_name>")
            sys.exit(1)
        arguments = sys.argv
        instance_name = arguments[1]
        client = boto3.client('ec2')               
               
        tags  = existing_tags(client,instance_name)
        print(tags)
    
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    main_connection()