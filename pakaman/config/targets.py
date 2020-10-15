from abc import ABCMeta
from typing import List, Dict

import schema

TARGETS = {}


class TargetMeta(ABCMeta):
    def __init__(cls, name, bases, classdict):
        super().__init__(name, bases, classdict)
        TARGETS[cls.name] = cls


class Target(metaclass=TargetMeta):
    name = "unknown"
    schema = schema.Schema({"name": str, schema.Optional("dependencies"): [str]}, ignore_extra_keys=True)

    def __init__(self, dependencies: List[str]):
        self.dependencies = dependencies

    @classmethod
    def from_config(cls, config: Dict) -> "Target":
        data = cls.schema.validate(config)
        if data["name"] not in TARGETS:
            raise KeyError(f"unknown target {data['name']} given in config file")

        data["dependencies"] = data.get("dependencies", [])

        target = TARGETS[data.pop("name")]
        target_data = target.schema.validate(config)

        return target(**data, **target_data)


class Debian(Target):
    name = "debian"
    schema = schema.Schema(
        {"dist_version": str, schema.Optional("compat_version", default=11): int, "architecture": str},
        ignore_extra_keys=True)

    def __init__(self, dependencies: List[str], dist_version: str, compat_version: int, architecture: str):
        super().__init__(dependencies)
        self.dist_version = dist_version
        self.compat_version = compat_version
        self.architecture = architecture


class Arch(Target):
    name = "arch"
    schema = schema.Schema({}, ignore_extra_keys=True)
