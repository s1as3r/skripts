#! /usr/bin/env python3
from os import listdir
import click

from mutagen.easyid3 import ID3
from mutagen.id3 import USLT
from providers import genius as gen, musixmatch


def apply_lyrics(song_path: str, lyrics_url: str) -> None:
    """
    `song_path` `str`: Path to the Song.
    `lyrics_url` `str`: Genius Url of the Song.
    """

    song = ID3(song_path)

    try:
        lyrics = provider.get_lyrics(lyrics_url)

        USLTOutput = USLT(encoding=3, lang=u"eng", desc=u"desc", text=lyrics)
        song["USLT::'eng'"] = USLTOutput

        print("Sucessfully Applied Lyrics to ", song_path)
    except:
        print("Can't apply lyrics to ", song_path)
        pass

    song.save(v2_version=3)


@click.group()
@click.option("--genius/--musixmatch", default=False, help="Provider to be used.")
def cli(genius):
    global provider
    if genius:
        provider = gen
    else:
        provider = musixmatch


@cli.command(help="Apply lyrics to all the songs in the current working directory")
def apply():
    for i in listdir():
        if ".mp3" in i or ".m4a" in i:
            apply_lyrics(i, provider.get_url(i[:-4]))


@cli.command(help="search for a song's lyrics")
@click.argument("song", type=str)
@click.option("--file", "-f", default="", help="file to apply the lyrics to")
def search(song, file):
    if file:
        apply_lyrics(file, provider.get_url(song))
    else:
        url = provider.get_url(song)
        lyrics = provider.get_lyrics(url)
        print(lyrics)


if __name__ == "__main__":
    cli()
