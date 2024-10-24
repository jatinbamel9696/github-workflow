#!/bin/bash

# Usage: ./putty-validation.sh <INSTANCE_ID>
# Ensure that the necessary parameters are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <INSTANCE_ID>"
    exit 1
fi

INSTANCE_ID=$1
REPORT_FILE="validation_report.txt"  # Report file name
USER="ec2-user"  # Change this if your instance uses a different user
KEY_PATH="./my-key"  # Path to your SSH private key in the same repo
HOSTNAME=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text)

# Check if the hostname is retrieved
if [ -z "$HOSTNAME" ]; then
    echo "Failed to retrieve hostname for instance ID: $INSTANCE_ID"
    echo "Validation failed for instance ID: $INSTANCE_ID" >> "$REPORT_FILE"
    exit 1
fi

# Set permissions for the private key (if needed)
chmod 600 "$KEY_PATH"

# Start validation report
echo "Validation Report for Instance ID: $INSTANCE_ID" > "$REPORT_FILE"
echo "--------------------------------------------------" >> "$REPORT_FILE"
echo "Hostname: $HOSTNAME" >> "$REPORT_FILE"

# Validate the connection using PuTTY
echo "Connecting to $HOSTNAME with user $USER..."
if putty -i "$KEY_PATH" "$USER@$HOSTNAME" -m commands-to-run.txt; then
    echo "Validation successful!" >> "$REPORT_FILE"
else
    echo "Validation failed!" >> "$REPORT_FILE"
fi

# Append additional validation details to the report
echo "Validation completed on: $(date)" >> "$REPORT_FILE"
echo "--------------------------------------------------" >> "$REPORT_FILE"
echo "Instance ID: $INSTANCE_ID" >> "$REPORT_FILE"
echo "User: $USER" >> "$REPORT_FILE"
echo "Private Key Path: $KEY_PATH" >> "$REPORT_FILE"
echo "--------------------------------------------------" >> "$REPORT_FILE"

# Display report contents
echo "Validation report created: $REPORT_FILE"
cat "$REPORT_FILE"
