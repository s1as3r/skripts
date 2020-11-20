import concurrent.futures
from os import chdir, mkdir
from os.path import exists
from sys import argv as args

from bs4 import BeautifulSoup
from requests import get

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}


def download_image(image_obj, num):
    base_url = 'https://wallpaperaccess.com/'
    image_url = base_url + image_obj.a['href']
    image_name = image_obj.find('span').text

    if exists(x := str(num)+'.jpg'):
        print(f'Skipping {image_name}')
        return

    print(f'Downloading {image_name} to {x}')
    image_bytes = get(image_url, headers=headers)

    with open(x, 'wb') as f:
        for chunk in image_bytes.iter_content(100000):
            f.write(chunk)


def main():
    if len(args) > 1:
        for url in args[1:]:
            print('Downloading images from ', url)
            soup = BeautifulSoup(get(url, headers=headers).text, 'html.parser')
            images = soup.find_all('div', {'class': 'wrapper'})

            try:
                mkdir(directory := url.split('/')[-1])
            except:
                pass

            chdir(directory)
            images_dict = dict(enumerate(images, 1))

            with concurrent.futures.ThreadPoolExecutor() as downloader:
                downloader.map(download_image, images_dict.values(), images_dict.keys())

            chdir('..')
    else:
        print(
            'No Argument Given',
            '\nPlease Provide a link to a WalpaperAcess Page'
            )

if __name__ == "__main__":
    main()
