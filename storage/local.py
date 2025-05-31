# storage/local.py
import os
import shutil
from storage.base import Storage
from config import settings


class LocalStorage(Storage):
    """
    LocalStorage is a concrete implementation of the Storage abstract base class.
    It provides methods to save files to the local filesystem, download files,
    and retrieve URLs for files stored locally.
    """

    def __init__(self, base_dir=None):
        self.base_dir = base_dir or settings.ASSET_LOCAL_DIR
        os.makedirs(self.base_dir, exist_ok=True)

    def save(self, fileobj, filename: str) -> str:
        """
        Save a file-like object to local storage.
        :param fileobj: The file-like object to save.
        :param filename: The name of the file to save.
        :return: The filename or path where the file was saved.
        """
        dest_path = os.path.join(self.base_dir, filename)
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(fileobj, f)
        return filename

    def download(self, filename: str, dest_path: str) -> None:
        """
        Download a file from local storage to a specified destination path.
        :param filename: The name of the file to download.
        :param dest_path: The local path where the file should be saved.
        """
        if not os.path.exists(self.base_dir):
            raise FileNotFoundError(f"Base directory {self.base_dir} does not exist.")
        src = os.path.join(self.base_dir, filename)
        shutil.copy(src, dest_path)

    def get_url(self, filename: str) -> str:
        """
        Get the URL of a file stored in local storage.
        :param filename: The name of the file for which to get the URL.
        :return: The URL of the file.
        """
        # For local, this could return a relative/static URL
        return f"/assets/files/{filename}"

