import os
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from mixver.cli.visualizer import show_tags
from mixver.versioning.versioner import Versioner


@dataclass
class LocalStorage:
    """
    Local storage to version ML models.

    Attributes:
        storage_path (str): Local path to use as storage.
        _versioner (Versioner): Artifacts versioning manager.
    """

    storage_path: str
    _versioner: Versioner = field(init=False)

    def __post_init__(self) -> None:
        """
        Create the storage.
        """
        # TODO: Handle complex paths or random names
        if not os.path.isdir(self.storage_path):
            os.mkdir(self.storage_path)

        self._versioner = Versioner(storage_path=self.storage_path)

    def push(
        self, artifact: Any, name: str, metadata: Dict, tags: Optional[list[str]] = None
    ) -> str:
        """
        Save data into the storage.
        """
        data = {
            "artifact": artifact,
            "metadata": metadata,
        }

        filename = self._versioner.add_artifact(name=name, tags=tags)

        with open(Path(self.storage_path, f"{filename}.pkl"), "wb") as file:
            pickle.dump(data, file)

        return filename

    def pull(self, tag: str = "", name: str = "", version: str = "") -> Dict:
        """
        Retrieve data from the storage.
        """
        if tag:
            filename = self._versioner.get_artifact_by_tag(tag=tag)
        elif name:
            filename = self._versioner.get_artifact_by_version(
                name=name, version=version
            )
        else:
            message = (
                "The identifier must be an integer to identify an artifact by its version or "
                "a string to identify the artifact by its tag."
            )
            raise ValueError(message)

        with open(Path(self.storage_path, f"{filename}.pkl"), "rb") as file:
            data = pickle.load(file)

        return data

    def visualize(self):
        """
        Visualize the tags and their associated artifacts.
        """
        tags, names, versions, paths = self._versioner.get_tags_data_for_visualization()
        show_tags(tags, names, versions, paths)
