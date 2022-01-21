#! /usr/bin/env python3
import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

import yaml
from jikanpy import Jikan


def get_all_eps(name: str) -> Dict[int, Tuple[str, bool]]:
    """
    `str` `name`: Name of the anime.

    RETURNS `Dict<int, Tuple<str, bool>>`: A dictionary containing an
    episode's name and filler info.

    Get all the episodes of an anime.
    """
    client = Jikan()

    results = client.search("anime", name)["results"][:10]
    anime = {i: j for i, j in enumerate(results, 1)}
    prompt = "\n".join(f"{n:0>2} => {t['title']}" for n, t in anime.items())
    selection = input(prompt + "\nSelect Anime: ")
    anime_id = anime[int(selection)]["mal_id"]
    selected_anime = client.anime(anime_id, extension="episodes")
    eps = selected_anime["episodes"]
    eps_len = selected_anime["episodes_last_page"]
    if eps_len != 1:
        for i in range(2, eps_len + 1):
            eps.extend(client.anime(anime_id, extension="episodes", page=i)["episodes"])

    ep_dict = {i["episode_id"]: [i["title"], i["filler"]] for i in eps}
    return ep_dict


def save_eps(name: str, eps: Dict[int, Tuple[str, bool]]) -> None:
    """
    `str` `name`: name of the file
    `Dict<int, Tuple<str, bool>>` `eps`: An episodes dict as returned by
    `get_all_eps`

    Saves the episodes' names in a yaml file.
    """
    with open(f"{name}.yml", "w") as f:
        ep_names = {i: j[0] for i, j in eps.items()}
        f.write(yaml.safe_dump(ep_names))


def parse_eps_arg(args: List[str]) -> List[int]:
    """
    `List<str>` `args`: A list of strings that are numbers
    and/or a range (e.g [1, 2, 4, 6-9])

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


def apply(eps_data: Dict[int, Tuple[str, bool]], regex: str):
    """
    `Dict<int, Tuple<str, bool]]` `eps_data`: An episodes dict as returned by
    `get_all_eps`

    `str` `regex`: A regular expression that matches the filenames.
    Must capture episode number and file extension.
    """

    re_pat = re.compile(regex, re.I)
    for item in os.listdir():
        m = re_pat.match(item)
        if m is not None:
            ep_no = m.groups()[0]
            ext = m.groups()[1]
            ep_name = eps_data.get(int(ep_no))

            if ep_name is not None:
                if sys.platform == "win32":
                    ep_name = ep_name[0].replace("/", ",").replace(":", "-")
                    ep_name = "".join(i for i in ep_name if i not in "\\*?<>|")
                os.rename(item, f"{ep_no} - {ep_name[0]}.{ext}")
            else:
                print(f"{ep_no} not in provided data")
        else:
            print(f"{regex} doesn't match {item}")


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
    parser.add_argument(
        "--apply",
        "-a",
        action="store_true",
        help="Rename anime in the current directory appropriately\n"
        + "Use in combination with --regex for best results.",
    )
    parser.add_argument(
        "--regex",
        "-r",
        metavar="REGEX",
        type=str,
        default=r"(\d+).(.*)",
        help="Regural Expression used to extract the episode no and the file extension"
        + " from an anime file.\nThe episode no and the extension must be captured.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    eps_dict = get_all_eps(args.name)
    if len(eps_dict) == 0:
        print(f"Cannot find anime named: {args.name}")
        sys.exit()

    if args.apply:
        apply(eps_dict, args.regex)
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
