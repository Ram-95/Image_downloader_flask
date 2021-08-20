'''RG Scrapper'''

import os
import random
import shutil
import inspect
import string
import bs4 as bs
import urllib.request
import requests
import time
import concurrent.futures


class RG:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
        self.base = 'https://www.ragalahari.com'
        self.response = requests.get(self.url, self.headers)
        self.html = self.response.text
        self.soup = bs.BeautifulSoup(self.html, 'lxml')
        self.ext = '.jpg'
        # If status_code is 200 then page exists. So it is a valid URL.
        if self.response.status_code == 200:
            self.invalid_url = False
        else:
            self.invalid_url = True
        self.paging_exists = self.soup.find('td', id='pagingCell')
        if self.paging_exists:
            self.t = self.paging_exists.findAll('a', class_='otherPage')
        else:
            self.t = None

    def _no_of_pages(self):
        '''Returns the number of pages.'''
        return len(self.t) if self.t is not None else 0

    def get_page_urls(self):
        '''Scrapes the urls of respective pages and saves it in a list.'''
        pages_url_list = []
        pages_url_list.append(self.url)
        pages = self._no_of_pages()
        for i in range(pages):
            pages_url_list.append(self.base + self.t[i]['href'])
        print('Page URLs captured')
        return pages_url_list

    def download_images(self, page_no):
        '''Scrapes the urls of images and saves them in list.'''
        global count

        gallery_exists = self.soup.find('div', id='galdiv')
        d = gallery_exists.findAll('img', class_='thumbnail')
        if d is None or d == []:
            d = gallery_exists.findAll('img')

        print(f'Page {page_no}: Downloading Images...\n')
        '''Code for Downloading the Images.'''
        for i in d:
            x = i['src']
            x = x.replace('t.jpg', '.jpg')
            # Downloading Code
            r = requests.get(x, stream=True)
            with open(str(count) + self.ext, 'wb') as outfile:
                outfile.write(r.content)
            count += 1

        print(f'Page {page_no}: {count} Images Download Complete.\n\n')

    def create_dir(self, base_dir):
        # Generates a alpha-numberic random name of length = 6
        name = 'RG_' + \
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
    rg = RG(page)
    img_urls = []
    gallery_exists = rg.soup.find('div', id='galdiv')
    d = gallery_exists.findAll('img', class_='thumbnail')
    if d is None or d == []:
        d = gallery_exists.findAll('img')
    for i in d:
        x = i['src']
        x = x.replace('t.jpg', '.jpg')
        img_urls.append(x)
    
    return img_urls


def download_images(img_url: str) -> None:
    title = img_url.split('/')[-1]
    r = requests.get(img_url, stream=True)
    with open(title, 'wb') as outfile:
        outfile.write(r.content)


# Driver Code
''' Function that initiates scrapping. '''
def start(url):
    # Creating an RG object
    start = time.perf_counter()
    rg = RG(url)
    if rg.invalid_url == False:
        # Global variable - Base directory
        base_dir = os.getcwd()

        # Getting the Page URLs
        pages = rg.get_page_urls()
        #print(pages, sep="\n")

        # Creating a Random directory
        dir_name = rg.create_dir(base_dir)
        caption = url.split('/')[-1].split('.')[0]

        global_img_urls = []
        ### Threads to get all the image urls from each page
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for res in executor.map(get_image_urls, pages):
                global_img_urls += res
        
        #### Threads to download images
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(download_images, global_img_urls)
        
        # Navigation to the base directory after downloading is complete
        os.chdir(base_dir)

        # Zipping files
        rg.zip_images(dir_name)

        # Deleting the gallery directory
        shutil.rmtree(dir_name)
        print(f'Main directory deleted: {dir_name}')
        finish = time.perf_counter()
        print(f'Time Taken: {round(finish-start,2)} second(s).\n')
        
    else:
        print('\nInvalid URL\n')
    return (rg.invalid_url, dir_name)
