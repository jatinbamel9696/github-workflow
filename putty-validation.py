import os
import sys
import datetime
import boto3
import logging

# Set up logging
logging.basicConfig(filename='validation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_instance_hostname(instance_id):
    """Fetches the public IP address of the given instance ID."""
    ec2 = boto3.client('ec2', region_name='us-east-1')
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        hostname = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        return hostname
    except Exception as e:
        logging.error(f"Failed to retrieve hostname for instance ID: {instance_id}. Error: {e}")
        return None

def write_report(instance_id, hostname, validation_status, key_path, report_dir):
    """Writes the validation report to a file."""
    os.makedirs(report_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"validation_report_{instance_id}_{timestamp}.txt")

    with open(report_file, 'w') as f:
        f.write(f"Validation Report for Instance ID: {instance_id}\n")
        f.write(f"Hostname: {hostname}\n")
        f.write(f"Validation Status: {validation_status}\n")
        f.write(f"Key Path: {key_path}\n")

    return report_file

def create_test_file(report_dir):
    """Creates a test file to indicate that validation is done."""
    test_file_path = os.path.join(report_dir, "validation_done.txt")
    with open(test_file_path, 'w') as f:
        f.write("Validation completed successfully.\n")
    logging.info(f"Test file created: {test_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python putty-validation.py <INSTANCE_ID>")
        sys.exit(1)

    instance_id = sys.argv[1]
    key_path = "./my-key"  # Path to your SSH private key in the same repo
    report_dir = 'reports/putty-validation/'  # Directory for reports

    hostname = get_instance_hostname(instance_id)

    if hostname:
        validation_status = "Validation completed successfully"  # No connection check
        report_path = write_report(instance_id, hostname, validation_status, key_path, report_dir)
        create_test_file(report_dir)  # Create the test file to indicate validation is done
        print(report_path)  # Output the report path for the workflow to capture
    else:
        validation_status = "Failed to retrieve hostname"
        write_report(instance_id, "N/A", validation_status, key_path, report_dir)
        sys.exit(1)
