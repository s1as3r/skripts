from bs4 import BeautifulSoup
from mutagen.easyid3 import ID3
from mutagen.id3 import USLT
from requests import get

# Access Token Already Provided.
headers = {
    'Authorization': 'Bearer alXXDbPZtK1m2RrZ8I4k2Hn8Ahsd0Gh_o076HYvcdlBvmc0ULL1H8Z8xRlew5qaG',
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}


def get_lyrics(url: str) -> str:
    '''
    `str` `url`: Genius URL of the song of which the lyrics are to be scraped.

    returns `str`: Lyrics of the song

    Scrapes the lyrics of the song.
    '''

    page = get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.select_one('div.lyrics').get_text().strip()

    return lyrics


def get_url(query: str) -> dict:
    '''
    `str` `query`: Search Query.

    returns `str`: The genius url of the song.

    Gets the genius lyrics url of the song.
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

