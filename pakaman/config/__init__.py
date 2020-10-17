import logging
from abc import ABCMeta, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Callable

import schema
import yaml

from .targets import Target

logger = logging.getLogger(__name__)

CONFIG_SCHEMA = schema.Schema(
    {
        "name": str,
        "language": str,
        schema.Optional("license"): str,
        schema.Optional("url"): str,
        schema.Optional("description"): str,
        "maintainer": {
            "name": str,
            "email": str
        },
        schema.Optional("install"): {
            schema.Optional("systemd"): [{
                "file": str,
                schema.Optional("enabled", default=False): bool,
                schema.Optional("started", default=False): bool
            }]
        },
        "changelog":
            [
                {
                    "version": str,
                    "urgency": str,
                    "changes": [str],
                    "date": datetime,
                    "author": {
                        "name": str,
                        "email": str
                    }
                }
            ],
        "distributions": [dict]
    }
)
LANGUAGES: Dict[str, Callable] = {}


class InvalidConfigException(Exception):
    pass


class ChangelogChange:
    def __init__(self, version: str, changes: List[str], urgency: str, date: datetime, author_name: str,
                 author_email: str):
        self.version = version
        self.changes = changes
        self.urgency = urgency
        self.date = date
        self.author_name = author_name
        self.author_email = author_email


class Changelog:
    def __init__(self, changes: List[ChangelogChange]):
        self.changes = changes

    @classmethod
    def from_dict(cls, changelog: List[Dict]) -> "Changelog":
        changes = [
            ChangelogChange(
                version=change["version"],
                changes=change["changes"],
                date=change["date"],
                urgency=change["urgency"],
                author_email=change["author"]["email"],
                author_name=change["author"]["name"]
            ) for change in changelog
        ]
        # sort by version
        changes = list(sorted(changes, key=lambda x: x.version, reverse=True))

        return cls(changes)


class Package:
    def __init__(
            self,
            name: str,
            language: str,
            changelog: Changelog,
            targets: List[Target],
            package_root: Path,
            maintainer_name: str,
            maintainer_email: str,
            systemd: Optional[Dict] = None,
            description: Optional[str] = None,
            long_description: Optional[str] = None,
            license: Optional[str] = None,
            url: Optional[str] = None
    ):
        self.name = name
        self.language = language
        self.changelog = changelog
        self.targets = targets
        self.maintainer_name = maintainer_name
        self.maintainer_email = maintainer_email
        self.package_root = package_root
        self.systemd = systemd
        self.description = description
        self.long_description = long_description
        self.license = license or "unknown"
        self.url = url

    @property
    def version(self):
        return self.changelog.changes[0].version

    @classmethod
    def from_config_file(cls, file_path: Path) -> "Package":
        with open(file_path, "r") as f:
            data = yaml.load(f)

        try:
            data = CONFIG_SCHEMA.validate(data)
        except schema.SchemaError as e:
            logger.error(f"Invalid config file: {e}")
            raise InvalidConfigException() from e

        targets = [Target.from_config(dist) for dist in data["distributions"]]

        # by default we assume the package root to be at the config file location
        package_root = file_path.parent

        package = cls(
            name=data["name"],
            language=data["language"],
            description=data.get("description"),
            url=data.get("url"),
            license=data.get("license"),
            systemd=data.get("install", {}).get("systemd"),
            maintainer_name=data["maintainer"]["name"],
            maintainer_email=data["maintainer"]["email"],
            package_root=package_root,
            changelog=Changelog.from_dict(data["changelog"]),
            targets=targets
        )

        if data["language"] in LANGUAGES:
            lang_config: LanguageConfig = LANGUAGES[data["language"]](package_root)
            lang_config.parse(package)

        return package


class LanguageConfigMeta(ABCMeta):
    def __init__(cls, name, bases, classdict):
        super().__init__(name, bases, classdict)
        LANGUAGES[cls.lang] = cls


class LanguageConfig(metaclass=LanguageConfigMeta):
    lang = "unknown"

    def __init__(self, input_dir: Path):
        self.input_dir = input_dir

    @abstractmethod
    def parse(self, package: Package):
        """
        Parse language specific packaging configs and store them in the 'Package' definition.
        """
        pass


# initialize LANGUAGES dict
from . import python
