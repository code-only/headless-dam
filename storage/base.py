from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Abstract base class for storage systems.
    This class defines the interface for storage operations such as saving,
    downloading, and retrieving URLs for files.
    """

    @abstractmethod
    def save(self, fileobj, filename: str) -> str:
        """
        Abstract method to save a file object to storage.
        :param fileobj: The file-like object to save.
        :param filename: The name of the file to save.
        :return: The filename or path where the file was saved.
        """
        pass

    # Abstract method to save a file object to storage
    # and return the filename or path where it was saved.
    @abstractmethod
    def download(self, filename: str, dest_path: str) -> None:
        """
        Abstract method to download a file from storage.
        :param filename: The name of the file to download.
        :param dest_path: The local path where the file should be saved.
        """
        pass

    # Abstract method to download a file from storage
    # given its filename and save it to the specified destination path.
    @abstractmethod
    def get_url(self, filename: str) -> str:
        """
        Abstract method to get the URL of a file in storage.
        :param filename: The name of the file for which to get the URL.
        :return: The URL of the file.
        """
        pass

