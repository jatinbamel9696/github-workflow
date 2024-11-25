import boto3
import os
import logging
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def upload_to_s3(bucket_name, local_report_path, github_run_id, include_extensions=None, include_files=None):
    """
    Uploads specific reports to the specified S3 bucket with the folder structure Reports/Year/Month/Day/github_run_id/reports.

    Parameters:
        bucket_name (str): Name of the S3 bucket.
        local_report_path (str): Path to the local reports directory.
        github_run_id (str): GitHub Run ID.
        include_extensions (list): List of file extensions to include (e.g., ['.txt', '.json']).
        include_files (list): List of specific file names to include (e.g., ['report1.txt', 'summary.json']).
    """
    try:
        # Assume the AWS role using environment-provided credentials
        session = boto3.Session()
        s3_client = session.client("s3")

        # Generate the S3 key prefix based on the current date and GitHub Run ID
        current_date = datetime.utcnow()
        s3_prefix = f"Reports/{current_date.year}/{current_date.month}/{current_date.day}/{github_run_id}/"

        # Upload specific files from the local reports directory to S3
        for root, _, files in os.walk(local_report_path):
            for file in files:
                # Check if the file should be uploaded
                if include_extensions and not file.endswith(tuple(include_extensions)):
                    continue
                if include_files and file not in include_files:
                    continue

                local_file_path = os.path.join(root, file)
                s3_key = s3_prefix + file

                # Upload the file
                s3_client.upload_file(local_file_path, bucket_name, s3_key)
                logger.info(f"Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")

    except (BotoCoreError, ClientError) as e:
        logger.error(f"An error occurred while uploading to S3: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Get inputs from environment variables
    BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    LOCAL_REPORT_PATH = os.getenv("LOCAL_REPORT_PATH")  # Example: './reports'
    GITHUB_RUN_ID = os.getenv("GITHUB_RUN_ID")         # GitHub Run ID passed as an environment variable

    # Define the criteria for files to upload
    INCLUDE_EXTENSIONS = [".log", ".html"]  # Upload only .txt and .json files (update as needed)
    INCLUDE_FILES = ['aws.json']# Example: ['specific-report.txt', 'summary.json'], or set to None to ignore

    if not BUCKET_NAME or not LOCAL_REPORT_PATH or not GITHUB_RUN_ID:
        logger.error("Error: Ensure S3_BUCKET_NAME, LOCAL_REPORT_PATH, and GITHUB_RUN_ID are set as environment variables.")
    else:
        upload_to_s3(BUCKET_NAME, LOCAL_REPORT_PATH, GITHUB_RUN_ID, INCLUDE_EXTENSIONS, INCLUDE_FILES)
