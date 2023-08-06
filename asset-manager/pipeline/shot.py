from dataclasses import dataclass, asdict
from typing import List
import os

from .directory import Directory
from .asset import Asset


@dataclass(frozen=True)
class ShotMetadata:
    name: str
    description: str = ""


class Shot:
    def __init__(self, directory: Directory) -> None:
        """Open a shot in the given directory.
        
        This will load any existing metadata or save the default as needed.
        """
        self._directory = directory

        try:
            metadata = ShotMetadata(**directory.load_metadata())
        except FileNotFoundError:
            # the directory is created, but if this is a new show, it
            # might not have any metadata yet, so we can instead save
            # a default file
            metadata = ShotMetadata(name=directory.name())
            directory.save_metadata(metadata)

        self._metadata = metadata

    def metadata(self) -> ShotMetadata:
        """Returns the available metadata for this shot."""
        # we want to copy this metadata into a new instance
        # because editing it should not change this class unless
        # update_metadat is called specifically
        return ShotMetadata(**asdict(self._metadata))

    def update_metadata(self, metadata: ShotMetadata) -> None:
        """Modify the metadata for this shot."""
        # call save_metadata first in case it fails we don't want this
        # class to have bad data on it.
        self._directory.save_metadata(metadata)
        # also make a copy so that the caller can't further modify
        # the data that we have without calling update_metadata again
        self._metadata = ShotMetadata(**asdict(metadata))

    def assets_by_category(self, category: str) -> List[str]:
        """Get the list of assets of a given category in the pipeline.

        The order of the returned assets is undetermined.
        """
        entries = os.listdir(self._directory)
        entries.remove(self._directory.METADATA_FILE)

        assets: List = [str]

        for asset in entries:
            metadata_file_path = os.path.join(asset, Directory.METADATA_FILE)
            metadata_file = os.path.join(self._directory, metadata_file_path)
            with open(metadata_file, "r") as file:
                metadata_json = json.load(file)

                if metadata_json["category"] == category:
                    assets.append(asset)

        del assets[0]
        return assets

    def assets(self) -> List[str]:
        """Get the list of assets in the pipeline.

        The order of the returned assets is undetermined.
        """
        entries = os.listdir(self._directory)
        entries.remove(self._directory.METADATA_FILE)
        return entries

    def load_asset(self, name: str) -> Asset:
        """Load the data for an asset in the storage.

        Args:
            name: The name of the asset to load

        Raises:
            FileNotFoundError: if the shot does not exist
        """

        asset_dir = os.path.join(self._directory, name)
        directory = Directory(asset_dir)
        return Asset(directory)

    def create_asset(self, name: str, category: str = "") -> Asset:
        """Create a new asset inside the pipeline storage.

        Args:
            name: The name of the asset to create
            category: The category to assign the asset. If this is left empty, asset will have no category.

        Raises:
            FileExistsError: If the asset already exists
        """
        asset_dir = os.path.join(self._directory, name)
        directory = Directory.create(asset_dir)
        return Asset(directory, category)

    def archive(self, delete_original_folder: bool = False) -> None:
        """Archive this shot into a .zip file

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
        """Remove this shot and all associated data."""
        self._directory.delete()
