#! /usr/bin/python3
import argparse
import platform
from pprint import pprint
import re
from functools import partial
import os
from pathlib import Path
from typing import Callable, List, NamedTuple

import spotdl.download as spotdl
from spotdl.search import SpotifyClient, from_spotify_url

PLAYLIST_RE = re.compile("https?://open.spotify.com/playlist/*")

SpotifyClient.init(
    client_id="9fec59cd741a4692b5ae2ccb84a725af",
    client_secret="4e347cc3d2b74c93b20b57b6a5f75951",
    user_auth=False,
)

CLIENT = SpotifyClient()


class Song(NamedTuple):
    title: str
    artists: List[str]
    album: str
    url: str


class Diff(NamedTuple):
    to_delete: List[Path]
    to_download: List[Song]


def get_source(directory: Path) -> str:
    conf = directory / ".spotisync"
    if not conf.is_file():
        raise FileNotFoundError(f".spotisync not found inside {directory}")

    with conf.open("r") as f:
        url = f.read().strip()
        if PLAYLIST_RE.match(url) is None:
            raise ValueError(f"url inside .spotisync is not that of a spotify playlist")

        return url


def _song_from_track(playlist_track: dict) -> Song:
    return Song(
        title=playlist_track["track"]["name"],
        artists=[artist["name"] for artist in playlist_track["track"]["artists"]],
        album=playlist_track["track"]["album"]["name"],
        url=playlist_track["track"]["external_urls"]["spotify"],
    )


def get_playlist(url: str) -> List[Song]:
    playlist_resp = CLIENT.playlist(url)["tracks"]

    songs = list(map(_song_from_track, playlist_resp["items"]))
    while playlist_resp["next"]:
        playlist_resp = CLIENT.next(playlist_resp)

        if playlist_resp is None:
            break

        songs.extend(list(map(_song_from_track, playlist_resp["items"])))

    return songs


def get_diff(
    local_tracks: List[Path],
    playlist_tracks: List[Song],
    validator: Callable[[Path, Song], bool],
) -> Diff:
    return Diff(
        to_delete=[
            track
            for track in local_tracks
            if not any(map(partial(validator, track), playlist_tracks))
        ],
        to_download=[
            track
            for track in playlist_tracks
            if not any(map(partial(lambda x, y: validator(y, x), track), local_tracks))
        ],
    )


def download(tracks: List[Song]):
    with spotdl.DownloadManager() as downloader:
        song_list = list(map(lambda s: from_spotify_url(s.url), tracks))
        if song_list:
            downloader.download_multiple_songs(song_list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="SpotiSync", description="Sync local tracks with a spotify playlist."
    )
    parser.add_argument(
        "--url",
        "-u",
        help="use custom url instead of looking for .spotisync",
        metavar="URL",
    )
    parser.add_argument(
        "--directory", "-d", help="local directory to sync", default=".", metavar="DIR"
    )
    parser.add_argument(
        "--glob", "-g", help="glob that matches the local songs", default="*mp3"
    )
    parser.add_argument(
        "--template",
        "-t",
        help="song name template used to compare",
        default="{artists} - {title}",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        help="manually choose what to delete",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    directory = Path(args.directory)

    if args.url:
        with (directory / ".spotisync").open("w") as f:
            f.write(args.url)
        url = args.url
    else:
        url = get_source(directory)

    local_tracks = list(directory.glob(args.glob))
    playlist_tracks = get_playlist(url)

    def validator(p: Path, s: Song) -> bool:
        local_name = p.name.removesuffix(p.suffix).lower()
        name = args.template.format(
            artists=", ".join(s.artists),
            artist=s.artists[0],
            title=s.title,
            album=s.album,
        )
        if platform.system() == "Windows":
            name = "".join(c for c in name if c not in '\\/*?"<>|').replace(":", " - ")

        return local_name == name.lower()

    diff = get_diff(local_tracks, playlist_tracks, validator)

    deleted = []
    downloaded = []

    for track in diff.to_delete:
        conf = True
        if args.interactive:
            conf = input(f"delete: {track}? (y/n)")[0].lower() == "y"
        if conf:
            os.remove(track)
            deleted.append(track.name)

    download(diff.to_download)
    for track in diff.to_download:
        downloaded.append(f"{', '.join(track.artists)} - {track.title}")

    print("Deleted:")
    pprint(deleted)

    print("Downloaded:")
    pprint(downloaded)


if __name__ == "__main__":
    main()
