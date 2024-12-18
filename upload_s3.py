import boto3
import os
import logging
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def upload_to_s3(bucket_name, local_report_path, github_run_id):
    """
    Uploads all files from the local reports directory to the specified S3 bucket.

    Parameters:
        bucket_name (str): Name of the S3 bucket.
        local_report_path (str): Path to the local reports directory.
        github_run_id (str): GitHub Run ID.
    """
    try:
        # Assume the AWS role using environment-provided credentials
        session = boto3.Session()
        s3_client = session.client("s3")

        # Generate the S3 key prefix based on the current date and GitHub Run ID
        current_date = datetime.utcnow()
        s3_prefix = f"Reports/{current_date.year}/{current_date.month}/{current_date.day}/{github_run_id}/"

        # Ensure the local directory exists
        if not os.path.exists(local_report_path):
            logger.error(f"Local path '{local_report_path}' does not exist.")
            return

        # Upload all files from the local reports directory to S3
        for root, _, files in os.walk(local_report_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                s3_key = s3_prefix + file

                try:
                    # Upload the file
                    s3_client.upload_file(local_file_path, bucket_name, s3_key)
                    logger.info(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")
                except (BotoCoreError, ClientError) as upload_error:
                    logger.error(f"Failed to upload {file}: {upload_error}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Get inputs from environment variables
    BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    LOCAL_REPORT_PATH = os.getenv("LOCAL_REPORT_PATH")  # Example: './reports'
    GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")         # GitHub Run ID passed as an environment variable

    # Validate mandatory inputs
    if not BUCKET_NAME:
        logger.error("S3_BUCKET_NAME is required but not set.")
    elif not LOCAL_REPORT_PATH:
        logger.error("LOCAL_REPORT_PATH is required but not set.")
    elif not GITHUB_RUN_ID:
        logger.error("GITHUB_RUN_ID is required but not set.")
    else:
        upload_to_s3(BUCKET_NAME, LOCAL_REPORT_PATH, GITHUB_RUN_ID)
