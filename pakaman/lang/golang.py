from distutils.dir_util import copy_tree
from pathlib import Path

from . import LanguageBuilder


class GoBuilder(LanguageBuilder):
    lang = "go"

    def build(self, output_dir: Path):
        """
        Build the python package to the given output directory for further processing.
        Assumes output_dir already exists.
        """
        copy_tree(str(self.input_dir), str(output_dir))
