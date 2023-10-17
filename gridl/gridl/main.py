import sys
from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor

from decouple import config
from requests import get
from steamgrid import Game, SteamGridDB


def download_grids(game: str, num: int, sgdb_api_key: str):
    sgdb = SteamGridDB(sgdb_api_key)

    results = sgdb.search_game(game)

    if results is None or len(results) == 0:
        print(f"API returned no results for {game}", file=sys.stderr)
        return

    result = results[0]
    print(f"Found: {result}")
    download(result, num, sgdb_api_key)


def download(game: Game, num: int, sgdb_api_key: str):
    sgdb = SteamGridDB(sgdb_api_key)
    grids = sgdb.get_grids_by_gameid([game.id])

    if grids is None or len(grids) == 0:
        print(f"API returned no grids for {game}", file=sys.stderr)
        return

    grids_and_names = [
        (grid.url, game.name + f" - {grid.id}.{grid.mime.split('/')[-1]}")
        for grid in grids[:num]
    ]

    grids = [g[0] for g in grids_and_names]
    names = [g[1] for g in grids_and_names]

    print(f"Grids: {grids}")
    print(f"Names: {names}")

    with ThreadPoolExecutor(5) as executor:
        executor.map(download_image, grids, names)


def download_image(url: str, filename: str):
    print(f"Downloading: {filename} - {url}")
    resp = get(url)

    if not resp.ok:
        print(f"error downloading: {url}")
        return

    with open(filename, "wb") as f:
        f.write(resp.content)


def parse_args() -> Namespace:
    parser = ArgumentParser("GriDL")
    parser.add_argument("game", metavar="GAME", type=str, help="title of the game")
    parser.add_argument(
        "--num", "-n", metavar="N", type=int, help="download N grids", default=5
    )
    parser.add_argument(
        "--key",
        "-k",
        metavar="KEY",
        type=str,
        help="use KEY instead of taking it from the env",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    if args.key:
        api_key = args.key
    else:
        api_key = config("SGDAPIKEY")

    download_grids(args.game, args.num, api_key)


if __name__ == "__main__":
    main()
