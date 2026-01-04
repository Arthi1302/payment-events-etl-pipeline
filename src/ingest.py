import os
import boto3
from dotenv import load_dotenv

# -----------------------------------
# Load environment variables
# -----------------------------------
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

RAW_DATA_DIR = "data/raw"
S3_RAW_PREFIX = "raw"


def upload_files_to_s3():
    s3_client = boto3.client("s3", region_name=AWS_REGION)

    for file_name in os.listdir(RAW_DATA_DIR):
        file_path = os.path.join(RAW_DATA_DIR, file_name)

        if os.path.isfile(file_path):
            s3_key = f"{S3_RAW_PREFIX}/{file_name}"

            print(f"⬆ Uploading {file_name} to s3://{S3_BUCKET}/{s3_key}")

            s3_client.upload_file(
                Filename=file_path,
                Bucket=S3_BUCKET,
                Key=s3_key
            )

    print("✅ All files uploaded to S3 successfully")


if __name__ == "__main__":
    upload_files_to_s3()
