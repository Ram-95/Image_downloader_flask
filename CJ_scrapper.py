'''CJ Scrapper'''

import os
import random
import shutil
import inspect
import string
import bs4 as bs
import requests
import time
import concurrent.futures


class CJ:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
        self.base_url = 'https://www.cinejosh.com'
        self.response = requests.get(self.url, self.headers)
        self.html = self.response.text
        self.soup = bs.BeautifulSoup(self.html, 'lxml')
        self.ext = '.jpg'
        # If status_code is 200 then page exists. So it is a valid URL.
        if self.response.status_code == 200:
            self.invalid_url = False
        else:
            self.invalid_url = True

        # Check if the URL is a gallery URL
        self.is_gallery = self.soup.findAll(
            'div', class_='container-gal-thumbs')
        # If the URL is not a gallery URL, then set invalid_url to True
        if self.is_gallery is None or self.is_gallery == []:
            self.invalid_url = True

        self.paging_exists = self.soup.find('ul', class_='pagination')
        if self.paging_exists:
            self.t = self.paging_exists.findAll('li')
        else:
            self.t = None

    def _no_of_pages(self):
        '''Returns the number of pages.'''
        return len(self.t) if self.t is not None else 0

    def get_page_urls(self) -> list:
        '''Scrapes the urls of respective pages and saves it in a list.'''
        pages_url_list = []
        pages_url_list.append(self.url)
        pages = self._no_of_pages()
        for i in range(1, pages-1):
            pages_url_list.append(self.base_url + self.t[i].find('a')['href'])
        print('Page URLs captured')
        return pages_url_list

    def create_dir(self, base_dir):
        # Generates a alpha-numberic random name of length = 6
        name = 'CJ_' + \
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Directory where images will be downloaded
        gallery_name = os.path.join(base_dir, name)
        # Creating Gallery directory
        os.mkdir(gallery_name)

        # Navigating to the Gallery Directory
        os.chdir(gallery_name)

        print(f'Directory: {name} created successfully.\n')
        return gallery_name

    def zip_images(self, directory):
        try:
            '''Zips the contents of the Directory'''
            shutil.make_archive(directory, 'zip', directory)
            print(f'\nZip Successful.')
        except Exception as e:
            print(
                f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')


def get_image_urls(page: str) -> list:
    '''Gets the image urls from all the pages.'''
    cj = CJ(page)
    d = cj.soup.findAll('div', class_='container-gal-thumbs')
    img_urls = []
    if d is None or d == []:
        cj.invalid_url = True
        return cj.invalid_url
    for i in d:
        temp = cj.base_url + i.find('img', class_='img-thumbnail')['src']
        if '/small' in temp:
            temp = temp.replace('/small', '')

        if 'thumb' in temp:
            temp = temp.replace('thumb', 'normal')
        img_urls.append(temp)

    return img_urls


def download_imgs(img_url: str) -> None:
    '''Downloads the image at the given url'''
    title = img_url.split('/')[-1]
    r = requests.get(img_url, stream=True)
    with open(title, 'wb') as outfile:
        outfile.write(r.content)


''' Driver code '''
def start(url):
    # Creating an CJ Object
    cj = CJ(url)
    if cj.invalid_url == False:
        # Global variable - Base directory
        base_dir = os.getcwd()

        # Creating an CJ object
        cj = CJ(url)

        # Getting the Page URLs
        pages = cj.get_page_urls()

        # Creating a Random directory
        dir_name = cj.create_dir(base_dir)

        # Global variable to name the images
        global count
        count = 1

        global_img_urls = []
        #### Threads for Getting Image URLs from each page ####
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for res in executor.map(get_image_urls, pages):
                global_img_urls += res
        finish = time.perf_counter()
        print(f'Global Image URLs size: {len(global_img_urls)}')
        print(f'Get Image URLs: {round(finish-start,2)} second(s).')

        #### Threads for downloading images #####
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            executor.map(download_imgs, global_img_urls)
        finish = time.perf_counter()
        print(f'Downloading images took: {round(finish-start,2)} second(s).')

        # Extracting the gallery name
        caption = cj.soup.find('h1', itemprop='headline').text

        # Navigation to the base directory after downloading is complete
        os.chdir(base_dir)

        # Zipping files
        cj.zip_images(dir_name)

        # Deleting the gallery directory
        shutil.rmtree(dir_name)
        print(f'Main directory deleted: {dir_name}')

    else:
        print(f'\nInvalid URL.\n')

    return (cj.invalid_url, dir_name)
