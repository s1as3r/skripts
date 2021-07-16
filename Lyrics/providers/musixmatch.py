import bs4, requests

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

def get_url(query: str) -> str:
    '''
    `str` `query`: Search Query.

    returns `str`: The musixmatch url of the song.

    Gets the musixmatch lyrics url of the song.
    '''


    search_url = "https://www.musixmatch.com/search/" + query
    search_resp = requests.get(search_url, headers=headers)
    soup = bs4.BeautifulSoup(search_resp.text, "html.parser")
    urls = soup.select("a[href^='/lyrics/']")
    best_url = "https://www.musixmatch.com" + urls[0].get("href")
    return best_url

def get_lyrics(url: str) -> str:
    '''
    `str` `url`: musixmatch URL of the song of which the lyrics are to be scraped.

    returns `str`: Lyrics of the song

    Scrapes the lyrics of the song.
    '''
    resp = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    lyrics_paragraphs = soup.select("p.mxm-lyrics__content")
    lyrics = "\n".join(i.text for i in lyrics_paragraphs)

    return lyrics
