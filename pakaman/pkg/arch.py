import os
import shutil
import subprocess
from pathlib import Path

from . import TargetBuilder


class Arch(TargetBuilder):
    name = "arch"

    def render(self, dir_path: Path):
        self.loader.render_templates_to_dir(
            ["PKGBUILD.j2", "changelog.j2"],
            self.package,
            self.target,
            dir_path)

    def make_pkg(self, dir_path: Path):
        environ = os.environ.copy()
        environ["SRCDEST"] = str(dir_path)
        cur_dir_save = os.getcwd()
        os.chdir(dir_path)
        subprocess.run(["makepkg", "--force"], env=environ)
        os.chdir(cur_dir_save)

        if self.clean_up:
            for f in dir_path.glob("*"):  # type: Path
                if f.suffix != ".zst":
                    if f.is_dir():
                        shutil.rmtree(f)
                    else:
                        f.unlink()
