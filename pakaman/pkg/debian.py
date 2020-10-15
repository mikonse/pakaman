import logging
import os
import shutil
import subprocess
from pathlib import Path

from . import TargetBuilder


logger = logging.getLogger(__name__)


class Debian(TargetBuilder):
    name = "debian"

    def render(self, dir_path: Path):
        debian_control_dir = dir_path / "debian"
        if not debian_control_dir.exists():
            debian_control_dir.mkdir(parents=True, exist_ok=True)
        self.loader.render_templates_to_dir(
            ["changelog.j2", "compat.j2", "control.j2", "install.j2", "rules.j2", "copyright.j2"],
            self.package,
            self.target,
            debian_control_dir)

    def make_pkg(self, dir_path: Path):
        cur_dir_save = os.getcwd()
        os.chdir(dir_path)
        subprocess.run(["debuild", "-us", "-uc", "-rfakeroot"])
        os.chdir(cur_dir_save)

        if self.remove_build_files:
            shutil.rmtree(dir_path)
            dir_path.mkdir()

        for f in dir_path.parent.glob("*"):
            if f.suffix in [".build", ".buildinfo", ".changes", ".deb", ".dsc", ".tar.gz"]:
                logger.info(f"output {f.name}")
                shutil.move(str(f), str(dir_path))
