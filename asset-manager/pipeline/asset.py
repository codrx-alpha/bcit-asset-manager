import os
import json
import shutil
from dataclasses import dataclass, asdict

from .directory import Directory

@dataclass(frozen=True)
class AssetMetadata:
    name: str
    category: str
    description: str = ""


class Asset:
    def __init__(self, directory: Directory, category: str) -> None:
        """Open an asset in the given directory.

        This will load any existing metadata or save the default as needed.
        """
        self._directory = directory

        try:
            metadata = AssetMetadata(**directory.load_metadata())
        except FileNotFoundError:
            # the directory is created, but if this is a new show, it
            # might not have any metadata yet, so we can instead save
            # a default file
            metadata = AssetMetadata(name=directory.name(), category=category)
            directory.save_metadata(metadata)

        self._metadata = metadata

    def metadata(self) -> AssetMetadata:
        """Returns the available metadata for this shot."""
        # we want to copy this metadata into a new instance
        # because editing it should not change this class unless
        # update_metadat is called specifically
        return AssetMetadata(**asdict(self._metadata))

    def update_metadata(self, metadata: AssetMetadata) -> None:
        """Modify the metadata for this shot."""
        # call save_metadata first in case it fails we don't want this
        # class to have bad data on it.
        self._directory.save_metadata(metadata)
        # also make a copy so that the caller can't further modify
        # the data that we have without calling update_metadata again
        self._metadata = AssetMetadata(**asdict(metadata))

    def delete(self) -> None:
        """Remove this asset and all associated data."""
        self._directory.delete()



