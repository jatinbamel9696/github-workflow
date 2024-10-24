import boto3
import sys
import os

def upload_file_to_s3(file_name, bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Successfully uploaded {file_name} to S3 bucket {bucket} as {object_name}.")
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python upload_to_s3.py <FILE_NAME> <BUCKET_NAME>")
        sys.exit(1)

    file_name = sys.argv[1]
    bucket_name = sys.argv[2]

    # Determine the appropriate object name for S3
    object_name = None
    if "putty-validation" in file_name:
        object_name = f"reports/putty-validation/{os.path.basename(file_name)}"
    elif "instance-detail" in file_name:
        object_name = f"reports/instance-detail/{os.path.basename(file_name)}"

    # Check if object_name was assigned properly
    if not object_name:
        print("Error: Unable to determine the S3 object name based on the provided file name.")
        sys.exit(1)

    upload_file_to_s3(file_name, bucket_name, object_name)
