#! /usr/bin/env python3
import sys
import yaml
from jikanpy import Jikan
import argparse
from typing import Tuple, Dict, List


def get_all_eps(name: str) -> Dict[int, Tuple[str, bool]]:
    """
    `str` `name`: Name of the anime.

    RETURNS `Dict<int, Tuple<str, bool>>`: A dictionary containing an episode's name and filler info.

    Get all the episodes of an anime.
    """
    client = Jikan()

    anime_id = client.search("anime", name)["results"][0]["mal_id"]
    anime = client.anime(anime_id, extension="episodes")
    eps = anime["episodes"]
    l = anime["episodes_last_page"]
    if l != 1:
        for i in range(2, l + 1):
            eps.extend(client.anime(anime_id, extension="episodes", page=i)["episodes"])

    ep_dict = {i["episode_id"]: [i["title"], i["filler"]] for i in eps}
    return ep_dict


def save_eps(name: str, eps: Dict[int, Tuple[str, bool]]) -> None:
    """
    `str` `name`: name of the file
    `Dict<int, Tuple<str, bool>>`: An episodes dict as returned by `get_all_eps`

    Saves the episodes' names in a yaml file.
    """
    with open(f"{name}.yml", "w") as f:
        ep_names = {i: j[0] for i, j in eps.items()}
        f.write(yaml.safe_dump(ep_names))


def parse_eps_arg(args: List[str]) -> List[int]:
    """
    `List<str>` `args`: A list of strings that are numbers and/or a range (e.g [1, 2, 4, 6-9])
    
    RETURNS `List<int>`: A list of integers.
    """
    eps: List[int] = []
    for arg in args:
        if "-" in arg:
            start = int(arg.split("-")[0])
            end = int(arg.split("-")[1])
            eps.extend(range(start, end + 1))
        elif arg.isdigit():
            eps.append(int(arg))

    return eps


def parse_args() -> argparse.Namespace:
    """
    Parses commandline arguments.
    """
    parser = argparse.ArgumentParser(
        prog="AniName", description="Get Anime Episode Names"
    )
    parser.add_argument("name", help="anime name", type=str)
    parser.add_argument(
        "--eps",
        "-e",
        type=str,
        nargs="*",
        metavar="EPS",
        help="Get names of only EPS."
        + "EPS may also include a range of episodes e.g 1-5",
    )
    parser.add_argument(
        "--save", "-s", action="store_true", help="store the data as yaml file"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    eps_dict = get_all_eps(args.name)
    if len(eps_dict) == 0:
        print(f"Cannot find anime named: {args.name}")
        sys.exit()

    if args.save:
        save_eps(args.name, eps_dict)
        sys.exit()

    if not args.eps:
        for i, j in eps_dict.items():
            print(f"{i:>03} - {j[0]} (Filler = {j[1]})")
    else:
        eps = parse_eps_arg(args.eps)
        for i in eps:
            j = eps_dict[i]
            print(f"{i:>03} - {j[0]} (Filler = {j[1]})")


if __name__ == "__main__":
    main()
