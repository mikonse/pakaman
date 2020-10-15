from pathlib import Path

from . import TargetBuilder


class Arch(TargetBuilder):
    name = "arch"

    def render(self, dir_path: Path):
        self.loader.render_templates_to_dir(
            ["PKGBUILD.j2", "proto.install.j2"],
            self.package,
            self.target,
            dir_path)
