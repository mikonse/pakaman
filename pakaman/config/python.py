import logging
import os
from distutils.core import run_setup

from setuptools.dist import Distribution, _Distribution

from . import LanguageConfig, Package


logger = logging.getLogger(__name__)


class SetuptoolsConfig(LanguageConfig):
    lang = "python"

    def parse(self, package: Package):
        setup_script = self.input_dir / "setup.py"
        save_cur_dir = os.getcwd()
        os.chdir(self.input_dir)

        try:
            if setup_script.exists() and setup_script.is_file():
                dist_instance = run_setup(str(setup_script), stop_after="commandline")
            elif (self.input_dir / "setup.cfg").exists():
                logger.info(f"no setup.py provided in project, trying to run default setuptools")
                dist_instance = Distribution()
                _Distribution.parse_config_files(dist_instance, filenames=[str(self.input_dir / "setup.cfg")])
            else:
                raise FileNotFoundError(f"no setuptools setup.py or setup.cfg does not exist")
        finally:
            os.chdir(save_cur_dir)

        package.description = dist_instance.metadata.description
        package.long_description = dist_instance.metadata.long_description
        package.url = dist_instance.metadata.url
        package.license = dist_instance.metadata.license
