import json
import os
from dataclasses import dataclass, field
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Optional

from mixver.versioning.exceptions import ArtifactDoesNotExist, EmptyRegistry, EmptyTags


class JSONManager:
    """
    This class manages reading and writing JSON files.
    """

    def __init__(
        self,
        file_path: str,
        catch_exceptions: Optional[Exception] = JSONDecodeError,
        raise_exceptions: Optional[Exception] = None,
        write: bool = True,
    ):
        self.file_path = file_path
        self.catch_exception = catch_exceptions
        self.raise_exceptions = raise_exceptions
        self.read_file = None
        self.write_file = None
        self.data = None
        self.write = write

    def __enter__(self):
        self.read_file = open(self.file_path, mode="r", encoding="utf8")

        try:
            self.data = json.load(self.read_file)
        except self.catch_exception as exc:
            if self.raise_exceptions:
                raise self.raise_exceptions from exc
            self.data = {}

        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.read_file.close()

        if self.write:
            with open(self.file_path, mode="w", encoding="utf8") as write_file:
                json.dump(self.data, write_file)


@dataclass(frozen=True)
class Versioner:
    """
    Class that manages the artifacts versioning

    Attributes:
        storage_path (str): Path where to create the version and tag files.
        _version_file (str): Version filename.
        _tags_file (str): Tags filename.
    """

    storage_path: str
    _version_file: str = field(default=".versions.json", init=False)
    _tags_file: str = field(default=".tags.json", init=False)

    def __post_init__(self) -> None:
        """
        The post initilizer checks if the storage path already contains
        the versions and tags file. Otherwise, they are created.
        """
        version_filepath = Path(self.storage_path, self._version_file)
        tags_filepath = Path(self.storage_path, self._tags_file)

        if not os.path.isfile(version_filepath):
            with open(version_filepath, "a", encoding="utf8"):
                pass

        if not os.path.isfile(tags_filepath):
            with open(tags_filepath, "a", encoding="utf8"):
                pass

    def _get_last_version(self, versions_data: dict, name: str) -> int:
        """
        Get the latest version of an artifact.

        Args:
            versions_data (dict): Artifacts' versioning data.
            name (str): Artifact's name

        Returns:
            int: Latest artifact version.
        """
        versions = versions_data[name].keys()
        versions = list(map(int, versions))
        return max(versions)

    def add_artifact(self, name: str, tags: Optional[list[str]] = None) -> str:
        """
        Add an artifact to the system. In the case that the artifact already
        exists, its version will be upgraded.

        Args:
            name (str): Artifact's name.
            tags (list[str]): Artifact's tags. Default is []

        Returns:
            str: Artifact's filename.
        """
        with JSONManager(
            file_path=Path(self.storage_path, self._version_file)
        ) as version_data:
            if name in version_data:
                new_version = self._get_last_version(version_data, name) + 1
            else:
                new_version = 1
                version_data[name] = {}

            filename = f"{name}_{new_version}"
            version_data[name][new_version] = filename

        if tags:
            with JSONManager(
                file_path=Path(self.storage_path, self._tags_file)
            ) as tags_data:
                for tag in tags:
                    tags_data[tag] = {name: {str(new_version): f"{name}_{new_version}"}}

        return filename

    def update_tags(self, name: str, tags: list[str], version: str = "") -> None:
        """
        Update the tags with a given artifact. In the case that no version is passed,
        it uses the latest version of that artifact.

        Args:
            name (str): Artifact's name.
            tags (list[str]): List of tags to be updated.
            version (str): Artifact's version. Default is empty, which means the
                latest version of the artifact will be used.
        """
        with JSONManager(
            file_path=Path(self.storage_path, self._version_file), write=False
        ) as version_data:
            if name not in version_data:
                raise ArtifactDoesNotExist(name)

            if not version:
                version = self._get_last_version(version_data, name)
            else:
                versions = version_data[name].keys()

                if not version in versions:
                    raise ArtifactDoesNotExist(name)

        with JSONManager(
            file_path=Path(self.storage_path, self._tags_file)
        ) as tags_data:
            for tag in tags:
                tags_data[tag] = {name: {str(version): f"{name}_{version}"}}

    def remove_artifact(self, name: str) -> None:
        """
        Remove an artifact from the registry.

        Args:
            name (str): Artifact's name.
        """
        with JSONManager(
            file_path=Path(self.storage_path, self._version_file)
        ) as version_data:
            if name not in version_data:
                raise ArtifactDoesNotExist(name)

            del version_data[name]

        with JSONManager(
            file_path=Path(self.storage_path, self._tags_file)
        ) as tags_data:

            for tag in tags_data.keys():
                if name in tags_data[tag]:
                    del tags_data[tag][name]

    def get_artifact_by_version(self, name: str, version: str = "") -> str:
        """
        Retrieves an artifact by its version. If the version is empty, the
        latest version will be returned.

        Args:
            name (str): Artifact's name.
            version (str): Artifact's version. Default is empty.

        Returns:
            str: Artifact's filepath.
        """
        with JSONManager(
            file_path=Path(self.storage_path, self._version_file),
            write=False,
            raise_exceptions=EmptyRegistry(),
        ) as version_data:
            if name not in version_data:
                raise ArtifactDoesNotExist(name)

            if not version:
                version = str(self._get_last_version(version_data, name))
            else:
                versions = version_data[name].keys()

                if not version in versions:
                    raise ArtifactDoesNotExist(name)

            filename = version_data[name][version]

        return filename

    def get_artifact_by_tag(self, tag: str) -> str:
        """
        Retrieves an artifact by its version. If the version is empty, the
        latest version will be returned.

        Args:
            tag (str): Tag assigned to the desired artifact.

        Returns:
            str: Artifact's filepath.
        """
        with JSONManager(
            file_path=Path(self.storage_path, self._tags_file),
            write=False,
            raise_exceptions=EmptyTags(),
        ) as tags_data:
            if tag not in tags_data:
                raise ArtifactDoesNotExist(tag, is_tag=True)

            name = list(tags_data[tag].keys())[0]
            filename = list(tags_data[tag][name].values())[0]

        return filename

    def get_tags_data_for_visualization(self):
        tags, names, versions, paths = [], [], [], []

        with JSONManager(
            file_path=Path(self.storage_path, self._tags_file),
            write=False,
            raise_exceptions=EmptyTags(),
        ) as tags_data:
            for tag in tags_data.keys():
                tags.append(tag)

                name = list(tags_data[tag].keys())[0]
                names.append(name)

                version = list(tags_data[tag][name].keys())[0]
                versions.append(version)

                filename = tags_data[tag][name][version]
                paths.append(filename)

            return tags, names, versions, paths
