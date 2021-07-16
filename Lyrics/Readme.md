# Lyrics
Chorus go repeeeeeaatttt!

Script to search/apply lyrics.

## Install
Either directly use `main.py` or install using `setup.py`/`pip`.

## Usage
- To search for lyrics of a song
    - `lyr search $song_name`
- To apply lyrics to a specific song
    - `lyr search $song_name -f $path-to-mp3/m4a-file`
    - To apply lyrics to all the songs in the current working direcory
        - `lyr apply`
        - Note: for this to work properly, the songs must be named in a good manner, e.g, 'NF - The Search.mp3'

### Providers
You can specify which provider to use by prepending `--musixmatch` or `--genius` when running `lyr`, e.g, `lyr --genius search "NF - Clouds"`