import os
from distutils.core import run_setup

from . import LanguageConfig, Package


class SetuptoolsConfig(LanguageConfig):
    lang = "python"

    def parse(self, package: Package):
        setup_script = self.input_dir / "setup.py"
        if not setup_script.exists() or not setup_script.is_file():
            raise FileNotFoundError(f"setuptools script {setup_script} does not exist")

        save_cur_dir = os.getcwd()
        os.chdir(self.input_dir)
        dist_instance = run_setup(str(setup_script), stop_after="commandline")
        os.chdir(save_cur_dir)
        package.description = dist_instance.metadata.description
        package.long_description = dist_instance.metadata.long_description
        package.url = dist_instance.metadata.url
        package.license = dist_instance.metadata.license
