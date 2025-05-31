# utils/s3_utils.py
import boto3
from typing import Optional
from botocore.exceptions import ClientError

from config import settings

S3_BUCKET = settings.S3_BUCKET
S3_ACCESS_KEY = settings.S3_ACCESS_KEY
S3_SECRET_KEY = settings.S3_SECRET_KEY
S3_REGION = settings.S3_REGION

s3_client = boto3.client("s3")


def download_file_from_s3(bucket: str, key: str, local_path: str) -> bool:
    """
    Download a file from S3 to a local path.
    :param bucket: S3 bucket name.
    :param key: S3 object key.
    :param local_path: Local path to save the downloaded file.
    :return: True if download was successful, False otherwise.
    """
    try:
        s3_client.download_file(bucket, key, local_path)
        return True
    except ClientError as e:
        print(f"S3 download error: {e}")
        return False


def upload_file_to_s3(local_path: str, bucket: str, key: str) -> bool:
    """
    Upload a file from a local path to S3.
    :param local_path: Local file path to upload.
    :param bucket: S3 bucket name.
    :param key: S3 object key.
    :return: True if upload was successful, False otherwise.
    """
    try:
        s3_client.upload_file(local_path, bucket, key)
        return True
    except ClientError as e:
        print(f"S3 upload error: {e}")
        return False


def get_s3_object_metadata(bucket: str, key: str) -> Optional[dict]:
    """
    Get metadata of an S3 object.
    :param bucket: S3 bucket name.
    :param key: S3 object key.
    :return: Metadata dictionary if successful, None otherwise.
    """
    try:
        response = s3_client.head_object(Bucket=bucket, Key=key)
        return response
    except ClientError as e:
        print(f"S3 metadata error: {e}")
        return None

