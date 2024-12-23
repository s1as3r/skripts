from argparse import ArgumentParser
from pathlib import Path
from sys import exit

ZIP_MAGIC = b"PK\x03\x04"


def get_zip_bytes(filepath: Path) -> bytes:
    assert filepath.suffix == ".exe", "provided file should be an exe"
    with open(filepath, "rb") as f:
        data = f.read()

    start = data.find(ZIP_MAGIC)
    if start == -1:
        print("given executable does not have a zip file in it")
        exit(1)

    return data[start:]


def get_parser() -> ArgumentParser:
    parser = ArgumentParser("love_src")
    parser.add_argument("game", metavar="GAME", type=Path, help="path to the game exe")
    parser.add_argument(
        "--output",
        "-o",
        metavar="OUT_PATH",
        type=Path,
        help="save the game source to %(metavar)s",
    )

    return parser


def main():
    args = get_parser().parse_args()
    zip_bytes = get_zip_bytes(args.game)

    output = args.output or args.game.parent / (args.game.stem + ".zip")

    with open(output, "wb") as f:
        f.write(zip_bytes)


if __name__ == "__main__":
    main()
