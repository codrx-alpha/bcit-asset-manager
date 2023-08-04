import os
import json
import shutil
from dataclasses import asdict
import zipfile
from typing import Any


class Directory(os.PathLike):
    """An existing directory where pipeline data is stored.

    Raises:
        FileNotFoundError: the directory does not yet exist
    """

    METADATA_FILE = "metadata.json"

    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self._root = path

    @staticmethod
    def create(path) -> "Directory":
        """Create a new pipeline directory for storing data."""
        os.mkdir(path)
        dir = Directory(path)
        return dir

    def __fspath__(self) -> str:
        return self._root

    def name(self) -> str:
        """The name of this directory on disk"""
        return os.path.basename(self._root)

    def load_metadata(self) -> dict:
        """Loads the current metadata from this directory."""

        metadata_file = os.path.join(self._root, Directory.METADATA_FILE)
        with open(metadata_file, "r") as file:
            return json.load(file)

    def save_metadata(self, metadata: dict) -> None:
        """Saves the given metadata into the directory for later retrieval.

        metadata: A data class holding the metadata to save
        """

        metadata_file = os.path.join(self._root, Directory.METADATA_FILE)
        with open(metadata_file, "w+") as file:
            json.dump(asdict(metadata), file)

    def delete(self) -> None:
        """Delete this directory and everything within it."""
        shutil.rmtree(self)
