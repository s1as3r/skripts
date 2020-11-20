from selenium import webdriver
from requests import get
import concurrent.futures
from os import mkdir, chdir
# from selenium.webdriver.common.action_chains import ActionChains


def download_image(url):
    file_name_pre = url.split('/')[-1]
    file_name = ''.join(i for i in file_name_pre if i.isalnum() or i in ' -_.')
    
    print(f'Downloading {file_name}')
    
    image_bytes = get(url)
    with open(file_name, 'wb') as f:
        for chunk in image_bytes.iter_content(100000):
            f.write(chunk)

if __name__ == "__main__":
    browser = webdriver.Chrome()

    browser.get('https://discord.com/app')
    print('Select The Server And Click On the Channel You Want To Download Images From and Then Press Enter here.')
    input('You Can also try and scroll to the top of the channel to get all the images.')

    server_name_pre = browser.find_element_by_class_name('name-1jkAdW').text
    server_name = ''.join(i for i in server_name_pre if i.isalnum() or i in ' -_.')
    # top_header = browser.find_element_by_class_name('header-3uLluP')
    # actions = ActionChains(browser)
    # actions.move_to_element(top_header).perform()
    image_elements = browser.find_elements_by_class_name('container-1ov-mD')

    image_links = []
    print('Fetching Image URLs')
    for image in image_elements:
        try:
            link = image.find_element_by_tag_name('a').get_attribute('href')
            image_links.append(link)
        except:
            continue
    
    browser.quit()

    try:
        mkdir(server_name)
    except FileExistsError:
        pass
    chdir(server_name)

    with concurrent.futures.ThreadPoolExecutor() as downloader:
        downloader.map(download_image, image_links)
