from argparse import ArgumentParser
from pathlib import Path


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="cf", description="count the number of files in a directory"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=Path("."),
        type=Path,
        help="directory to count the files in",
        metavar="DIR",
    )

    return parser


def count_files(dir: Path) -> int:
    return sum(i.is_file() for i in dir.glob("**/*"))


def main():
    args = get_parser().parse_args()
    print(count_files(args.directory))


if __name__ == "__main__":
    main()
