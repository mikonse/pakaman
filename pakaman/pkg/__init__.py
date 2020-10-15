from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional, Callable, Dict

from pakaman.config import Package, Target
from .assets import AssetLoader

TARGETS: Dict[str, Callable] = {}


def get_target(name: str) -> Optional[Callable]:
    return TARGETS.get(name)


class TargetMeta(ABCMeta):
    def __init__(cls, name, bases, classdict):
        super().__init__(name, bases, classdict)
        TARGETS[cls.name] = cls


class TargetBuilder(metaclass=TargetMeta):
    name = "unknown"

    def __init__(self, package: Package, target: Target, output_dir: Path, clean_up: bool):
        self.package = package
        self.target = target
        self.output_dir = output_dir
        self.clean_up = clean_up
        self.loader = AssetLoader(self.name)

    @abstractmethod
    def render(self, dir_path: Path):
        pass

    @abstractmethod
    def make_pkg(self, dir_path: Path):
        pass

    def build(self):
        self.render(self.output_dir)
        self.make_pkg(self.output_dir)


# initialize TARGETS dict
from . import arch, debian
