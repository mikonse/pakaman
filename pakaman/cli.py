import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from pakaman.builder import PackageBuilder
from pakaman.config import Package, InvalidConfigException

logging.basicConfig(format="%(asctime)s | %(name)-8s | %(levelname)-5s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Pakman - <insert os here> package builder")
    parser.add_argument("-c", "--config", type=str, default="pakaman.yaml", help="Path to pakman config file")
    parser.add_argument("-o", "--output", type=str, default="pakaman-build", help="Output directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--no-cleanup", action="store_true", help="Do not clean up build files")

    return parser


def cli():
    args = create_parser().parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    config_file = Path(args.config).absolute()
    if not config_file.exists() or not config_file.is_file():
        logger.error(f"Config file {config_file} not found")
        sys.exit(1)

    try:
        package = Package.from_config_file(config_file)
    except InvalidConfigException:
        sys.exit(1)

    output_dir = Path(args.output).absolute()

    builder = PackageBuilder(package, output_dir, clean_up=not args.no_cleanup)
    builder.build()


if __name__ == '__main__':
    cli()
