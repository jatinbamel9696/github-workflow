import os
import sys
import subprocess
import datetime
import boto3

def get_instance_hostname(instance_id):
    """Fetches the public IP address of the given instance ID."""
    ec2 = boto3.client('ec2', region_name='us-east-1')
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        hostname = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        return hostname
    except Exception as e:
        print(f"Failed to retrieve hostname for instance ID: {instance_id}. Error: {e}")
        return None

def write_report(instance_id, hostname, validation_status, key_path):
    """Writes the validation report to a file with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/putty-validation/validation_report_{instance_id}_{timestamp}.txt"
    
    with open(report_file, 'w') as f:
        f.write("Validation Report for Instance ID: {}\n".format(instance_id))
        f.write("--------------------------------------------------\n")
        f.write("Hostname: {}\n".format(hostname))
        f.write("Validation Status: {}\n".format(validation_status))
        f.write("Validation completed on: {}\n".format(datetime.datetime.now()))
        f.write("--------------------------------------------------\n")
        f.write("Instance ID: {}\n".format(instance_id))
        f.write("Private Key Path: {}\n".format(key_path))
        f.write("--------------------------------------------------\n")
    
    print(f"Validation report created: {report_file}")
    return report_file

def validate_connection(hostname, user, key_path):
    """Attempts to connect to the instance using PuTTY."""
    # Set permissions for the private key
    os.chmod(key_path, 0o600)
    
    print(f"Connecting to {hostname} with user {user}...")
    
    # Command to execute on the remote host, replace 'commands-to-run.txt' with the actual command you want to run
    command_to_run = f"putty -i {key_path} {user}@{hostname} -m commands-to-run.txt"
    
    # Execute the command
    try:
        result = subprocess.run(command_to_run, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "Validation successful!"
    except subprocess.CalledProcessError as e:
        print(f"Validation failed! Error: {e.stderr.decode('utf-8')}")
        return "Validation failed!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python putty-validation.py <INSTANCE_ID>")
        sys.exit(1)

    instance_id = sys.argv[1]
    user = "ec2-user"  # Change this if your instance uses a different user
    key_path = "./my-key"  # Path to your SSH private key in the same repo

    hostname = get_instance_hostname(instance_id)

    if hostname:
        validation_status = validate_connection(hostname, user, key_path)
        report_path = write_report(instance_id, hostname, validation_status, key_path)
        print(report_path)  # Output the report path for the workflow to capture
    else:
        write_report(instance_id, "N/A", "Failed to retrieve hostname", key_path)
        sys.exit(1)
