import os
from dataclasses import dataclass, asdict
from typing import List
import shutil

from .directory import Directory
from .shot import Shot


@dataclass(slots=True, eq=True)
class ShowMetadata:
    name: str
    description: str = ""


class Show:
    def __init__(self, directory: Directory) -> None:
        """Open a show in the given directory.
        
        This will load any existing metadata or save the default as needed.
        """
        self._directory = directory

        try:
            metadata = ShowMetadata(**directory.load_metadata())
        except FileNotFoundError:
            # the directory is created, but if this is a new show, it
            # might not have any metadata yet, so we can instead save
            # a default file
            metadata = ShowMetadata(name=directory.name())
            directory.save_metadata(metadata)

        self._metadata = metadata

    def metadata(self) -> ShowMetadata:
        """Returns the available metadata for this show."""
        # we want to copy this metadata into a new instance
        # because editing it should not change this class unless
        # update_metadat is called specifically
        return ShowMetadata(**asdict(self._metadata))

    def update_metadata(self, metadata: ShowMetadata) -> None:
        """Modify the metadata for this show."""
        # call save_metadata first in case it fails we don't want this
        # class to have bad data on it.
        self._directory.save_metadata(metadata)
        # also make a copy so that the caller can't further modify
        # the data that we have without calling update_metadata again
        self._metadata = ShowMetadata(**asdict(metadata))

    def shots(self) -> List[str]:
        """Get the list of shots in the pipeline.

        The order of the returned shots is undertermined.
        """
        entries = os.listdir(self._directory)
        entries.remove(self._directory.METADATA_FILE)
        return entries

    def load_shot(self, name: str) -> Shot:
        """Load the data for a shot in the storage.

        Args:
            name: The name of the shot to load

        Raises:
            FileNotFoundError: if the shot does not exist
        """

        shot_dir = os.path.join(self._directory, name)
        directory = Directory(shot_dir)
        return Shot(directory)

    def create_shot(self, name: str) -> Shot:
        """Create a new shot inside the pipeline storage.

        Raises:
            FileExistsError: If the shot already exists
        """

        shot_dir = os.path.join(self._directory, name)
        directory = Directory.create(shot_dir)
        return Shot(directory)

    def archive(self, delete_original_folder: bool = False) -> None:
        """Archive this show into a .zip file

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
        """Remove this show and all associated shots and data."""
        self._directory.delete()
