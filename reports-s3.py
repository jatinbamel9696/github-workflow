import boto3
import os
from datetime import datetime

def upload_report_to_s3(bucket_name, file_path):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Define the S3 key structure with timestamp in the filename
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%b")       # e.g., Oct
    date = now.strftime("%m_%d_%Y")  # e.g., 11_08_2024
    timestamp = now.strftime("%H-%M-%S")  # e.g., 15-30-45 for hours-minutes-seconds
    
    # Extract the original file name without extension and add the timestamp
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    s3_key = f"Verification_Report/{year}/{month}/{date}/{base_name}_{timestamp}.html"
    
    try:
        # Upload the file to S3
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Report uploaded successfully to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading report: {e}")

# Usage
bucket_name = "test-j3"
file_path = "reports/report.html"  # Direct file path
upload_report_to_s3(bucket_name, file_path)
