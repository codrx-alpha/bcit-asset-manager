from typing import List
import os

from .show import Show
from .directory import Directory


class Storage:
    def __init__(self, root: str) -> None:
        """Create a new pipeline storage.

        Args:
            root: The path under which all pipeline data is stored
        """
        # we want to make sure the path that we store is absolute
        # in case the current working directory changes in the future
        # we want to make sure this class instance uses the original one
        self._root = os.path.abspath(root)

    def shows(self) -> List[str]:
        """Get the list of shows in the pipeline.

        The order of the returned shows is undertermined.
        """
        entries = os.listdir(self._root)
        return entries

    def load_show(self, name: str) -> Show:
        """Load the data for a show in the storage.

        Args:
            name: The name of the show to load

        Raises:
            FileNotFoundError: if the show does not exist
        """

        show_dir = os.path.join(self._root, name)
        directory = Directory(show_dir)
        return Show(directory)

    def create_show(self, name: str) -> Show:
        """Create a new show inside the pipeline storage.

        Raises:
            FileExistsError: If the show already exists
        """

        show_dir = os.path.join(self._root, name)
        directory = Directory.create(show_dir)
        return Show(directory)
