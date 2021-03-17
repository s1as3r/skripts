#! /usr/bin/env python3
from os import listdir

from bs4 import BeautifulSoup # BeautifulSoup for scraping lyrics.
from mutagen.easyid3 import ID3# Mutagen for applying the meta tags to audio files.
from mutagen.id3 import USLT # USLT for applying lyrics to the audio file.
from requests import get # requests for handling all the HTTPS requests


# Access Token Already Provided.
headers = {
    'Authorization': 'Bearer alXXDbPZtK1m2RrZ8I4k2Hn8Ahsd0Gh_o076HYvcdlBvmc0ULL1H8Z8xRlew5qaG',
}


def scrape_song_lyrics(url: str) -> str:
    '''
    `str` `url`: Genius URL of the song of which the lyrics are to be scraped.

    returns `str`: Lyrics of the song

    Scrapes the lyrics of the song.
    '''
    
    page = get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', attrs={'class': 'lyrics'}).get_text()

    return lyrics


def get_url(query:str) -> dict:
    '''
    `str` `query`: Search Query.

    `bool` `romanized`: If True, searches for romanized lyrics.

    returns `dict`: A dictionary that contains metadata of the song.

    Gets the metadata of the song.
    '''
    
    search_query = '+'.join(i for i in query.split())

    search_url = 'https://api.genius.com/search'
    search_response = get(search_url, headers=headers,
                          params={'q': search_query}).json()['response']

    song_id = search_response['hits'][0]['result']['id']
    song_url = f'https://api.genius.com/songs/{song_id}'

    song_response = get(song_url,
                        headers=headers).json()['response']['song']
    
    lyrics_url = song_response['url']

    return lyrics_url


def apply_lyrics(song_path:str, lyrics_url:str) -> None:
    '''
    `song_path` `str`: Path to the Song.
    `lyrics_url` `str`: Genius Url of the Song.
    '''
    
    song = ID3(song_path)

    try:
        lyrics = scrape_song_lyrics(lyrics_url)
        
        USLTOutput = USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)
        song["USLT::'eng'"] = USLTOutput

        print('Sucessfully Applied Lyrics to ', song_path)
    except:
        print('Can\'t apply lyrics to ', song_path)
        pass

    song.save(v2_version=3)


def main():
    for i in listdir():
        if '.mp3' in i or '.m4a' in i:
            apply_lyrics(i, get_url(i[:-4]))
    

if __name__ == "__main__":
    main()
