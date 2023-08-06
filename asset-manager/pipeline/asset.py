import os
import json
import shutil
from dataclasses import dataclass, asdict
from typing import List
import shutil

from .directory import Directory

@dataclass(frozen=True)
class AssetMetadata:
    """A dataclass for storing information about an asset.

       Attributes:
           name (str): The name of the asset.
           category (str): The category of the asset.
           description (str): A description of the asset.
    """
    name: str
    category: str
    description: str = ""


class Asset:
    """A class for representing an asset in a given directory.

        Attributes:
            _directory (Directory): The directory where the asset is located.
            _metadata (AssetMetadata): The metadata associated with the asset.

        Methods:
            metadata: Returns the available metadata for this shot.
            update_metadata: Modify the metadata for this shot.
            shots: Get the list of shots this asset is used in.
            archive: Archive this asset into a .zip file.
            delete: Remove this asset and all associated data.
    """
    def __init__(self, directory: Directory, category: str = "") -> None:
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

    def shots(self) -> List[str]:
        """Get the list of shots this asset is used in.

        Asset must have the same name in other shots.

        The order of the returned shots is undetermined.
        """
        asset = self._directory.__fspath__()
        shot = os.path.dirname(asset)
        show = os.path.dirname(shot)

        shots = os.listdir(show)
        shots.remove(self._directory.METADATA_FILE)

        shot_path = os.path.split(asset)[0]
        show_path = os.path.split(shot_path)[0]

        related_shots: List = []

        for entry in shots:
            asset_path = os.path.join(entry, self._metadata.name)
            full_asset_path = os.path.join(show_path, asset_path)

            if os.path.exists(full_asset_path):
                related_shots.append(entry)
            else:
                pass

        return related_shots

    def archive(self, delete_original_folder: bool = False) -> None:
        """Archive this asset into a .zip file

        Args:
            delete_original_folder: If set to True, the directory being zipped will be deleted.

        """
        path = os.path.join(os.path.dirname(self._directory), self._directory)
        shutil.make_archive(path, "zip", path)

        if delete_original_folder:
            shutil.rmtree(path)
        else:
            pass

    def delete(self) -> None:
        """Remove this asset and all associated data."""
        self._directory.delete()



