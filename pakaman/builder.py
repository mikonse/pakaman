import logging
from pathlib import Path

from pakaman.config import Package, Target
from pakaman.lang import get_lang, LanguageBuilder
from pakaman.pkg import get_target, TargetBuilder

logger = logging.getLogger(__name__)


class PackageBuilder:
    def __init__(self, package: Package, output_dir: Path):
        self.package = package
        self.output_dir = output_dir

        lang_builder_cls = get_lang(self.package.language)
        if lang_builder_cls is None:
            raise ValueError(f"unknown language {self.package.language} given")

        self.lang_builder: LanguageBuilder = lang_builder_cls(self.package.package_root)

    def build_target(self, target: Target):
        out_dir = self.output_dir / target.name
        out_dir.mkdir(exist_ok=True, parents=True)
        self.lang_builder.build(out_dir)

        target_builder = get_target(target.name)
        if target_builder is None:
            raise KeyError(f"unknown build target {target.name}")
        builder: TargetBuilder = target_builder(self.package, target, out_dir)
        builder.build()

    def build(self):
        for target in self.package.targets:
            self.build_target(target)
