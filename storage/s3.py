# storage/s3.py
import boto3
from storage.base import Storage
from config import settings


# S3Storage is a concrete implementation of the Storage abstract base class.
class S3Storage(Storage):
    """
    S3Storage is a concrete implementation of the Storage abstract base class.
    It provides methods to save files to an S3 bucket, download files,
    and retrieve URLs for files stored in S3.
    """

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
        )
        self.bucket = settings.S3_BUCKET

    def save(self, fileobj, filename: str) -> str:
        self.client.upload_fileobj(fileobj, self.bucket, filename)
        return filename

    def download(self, filename: str, dest_path: str) -> None:
        self.client.download_file(self.bucket, filename, dest_path)

    def get_url(self, filename: str) -> str:
        # Create a presigned URL or use public URL if bucket is public
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": filename},
            ExpiresIn=3600,
        )

