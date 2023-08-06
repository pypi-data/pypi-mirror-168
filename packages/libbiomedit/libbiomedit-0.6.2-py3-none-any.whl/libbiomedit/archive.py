import tarfile
import zipfile
from abc import ABC, abstractmethod
from contextlib import contextmanager

# TODO: remove pylint disable, once we require python >= 3.9
from os import PathLike  # pylint: disable=unused-import
from typing import IO, List, Union, Generator

from . import unwrap


class ArchiveReaderInterface(ABC):
    @classmethod
    @abstractmethod
    def opener(
        cls,
        path: Union[
            str, "PathLike[str]"
        ],  # TODO: unquote PathLike typehint, once we require python >= 3.9
    ) -> Union["ZipReader", "TarReader"]:
        """Open archive for reading"""

    @staticmethod
    @abstractmethod
    def is_valid_type(path: Union[str, "PathLike[str]"]) -> bool:
        """Check if an archive file has a valid type"""

    @abstractmethod
    def namelist(self) -> List[str]:
        """Return a list of archive members by name"""

    @abstractmethod
    def extract_member(self, name: str) -> IO[bytes]:
        """Get a member from the archive as a file object"""


class ZipReader(zipfile.ZipFile, ArchiveReaderInterface):
    @classmethod
    def opener(cls, path: Union[str, "PathLike[str]"]) -> "ZipReader":
        return cls(path)

    @staticmethod
    def is_valid_type(path: Union[str, "PathLike[str]"]) -> bool:
        """Check if an archive file is a ZIP file"""
        return zipfile.is_zipfile(path)

    def extract_member(self, name: str) -> IO[bytes]:
        """Get a member from the archive as a file object"""
        try:
            return self.open(name)
        except KeyError as e:
            raise KeyError(f"File object {name} not found in {self.filename}") from e


class TarReader(tarfile.TarFile, ArchiveReaderInterface):
    @classmethod
    def opener(cls, path: Union[str, "PathLike[str]"]) -> "TarReader":
        return cls.open(path, format=tarfile.PAX_FORMAT)

    @staticmethod
    def is_valid_type(path: Union[str, "PathLike[str]"]) -> bool:
        """Check if an archive file is a TAR file"""
        return tarfile.is_tarfile(path)

    def namelist(self) -> List[str]:
        """Return a list of archive members by name"""
        return self.getnames()

    def extract_member(self, name: str) -> IO[bytes]:
        """Get a member from the archive as a file object"""
        try:
            return unwrap(self.extractfile(name))
        except (KeyError, ValueError) as e:
            raise KeyError(f"File object {name} not found in {str(self.name)}") from e


@contextmanager
def archive_reader(
    path: Union[str, "PathLike[str]"]
) -> Generator[Union[ZipReader, TarReader], None, None]:
    if ZipReader.is_valid_type(path):
        with ZipReader.opener(path) as zip_reader:
            yield zip_reader
    elif TarReader.is_valid_type(path):
        with TarReader.opener(path) as tar_reader:
            yield tar_reader
    else:
        raise TypeError(
            f"Input file '{path}' is not a .zip or .tar archive.\n"
            "Only .zip and .tar files can be used as input."
        )
