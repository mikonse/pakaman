from pathlib import Path
from typing import Dict, List

import jinja2

import pakaman
from pakaman.config import Package, Target


def get_asset_path() -> Path:
    base_dir = Path(pakaman.__file__).parent
    return base_dir / "assets"


class AssetLoader:
    def __init__(self, target: str):
        self.template_dir = get_asset_path() / "templates" / target
        self.template_loader = jinja2.FileSystemLoader(searchpath=str(self.template_dir))
        self.template_env = jinja2.Environment(loader=self.template_loader)

    def render_template(self, name: str, context: Dict):
        return self.template_env.get_template(name).render(**context)

    def render_template_to_file(self, name: str, package: Package, target: Target, to_file: Path):
        template = self.render_template(name, context={"package": package, "target": target})

        with open(to_file, "w+") as f:
            f.write(template)

    def render_template_to_dir(self, name: str, package: Package, target: Target, to_dir: Path):
        self.render_template_to_file(name, package, target, to_dir / str(Path(name).with_suffix("")))

    def render_templates_to_dir(self, templates: List[str], package, target: Target, to_dir: Path):
        for template in templates:
            self.render_template_to_dir(template, package, target, to_dir)

