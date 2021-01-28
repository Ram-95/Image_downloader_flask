import os
import random
import shutil
import inspect
import string
import bs4 as bs
import urllib.request
import requests
import Email_send as email


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
        self.is_gallery = self.soup.findAll('div', class_='container-gal-thumbs')
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

    def get_page_urls(self):
        '''Scrapes the urls of respective pages and saves it in a list.'''
        pages_url_list = []
        pages_url_list.append(self.url)
        pages = self._no_of_pages()
        for i in range(1, pages-1):
            pages_url_list.append(self.base_url + self.t[i].find('a')['href'])
        print('Page URLs captured')
        return pages_url_list

    def download_images(self, page_no):
        '''Scrapes the urls of images and saves them in list.'''
        global count
        d = self.soup.findAll('div', class_='container-gal-thumbs')
        if d is None or d == []:
            self.invalid_url = True
            return self.invalid_url
        
        print(f'Page {page_no}: Downloading Images...\n')
        for i in d:
            temp = self.base_url + i.find('img', class_='img-thumbnail')['src']
            if '/small' in temp:
                temp = temp.replace('/small', '')

            if 'thumb' in temp:
                temp = temp.replace('thumb', 'normal')
            # Downloading Code
            r = requests.get(temp, stream=True)
            with open(str(count) + self.ext, 'wb') as outfile:
                outfile.write(r.content)
            count += 1

        print(f'Page {page_no}: {count} Images Download Complete.\n\n')

    def create_dir(self, base_dir):
        # Generates a alpha-numberic random name of length = 6
        name = 'CJ_' + \
            ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Directory where images will be downloaded
        gallery_name = base_dir + name
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

    def send_mail(self, directory, caption):
        try:
            email.send_mail(directory, caption)
        except Exception as e:
            raise Exception(e)


''' Driver code '''
def start(url):
    # Creating an CJ Object
    cj = CJ(url)
    if cj.invalid_url == False:
        # Global variable - Base directory
        base_dir = os.getcwd() + '\\'

        # Creating an CJ object
        cj = CJ(url)

        # Getting the Page URLs
        pages = cj.get_page_urls()

        # Creating a Random directory
        dir_name = cj.create_dir(base_dir)
    
        # Global variable to name the images
        global count
        count = 1

        # Creating an CJ object of all the pages urls and downloading
        for i in range(len(pages)):
            cj = CJ(pages[i])
            cj.download_images(i+1)
        print(f'**** {count} images downloaded. ****')

        # Extracting the gallery name
        caption = cj.soup.find('h1', itemprop='headline').text

        # Navigation to the base directory after downloading is complete
        os.chdir(base_dir)

        # Zipping files
        cj.zip_images(dir_name)

        # Deleting the gallery directory
        shutil.rmtree(dir_name)
        print(f'Main directory deleted: {dir_name}')
        
        # Emailing the file
        cj.send_mail(os.path.basename(dir_name), caption)
    else:
        print(f'\nInvalid URL.\n')
    
    return (cj.invalid_url, dir_name)
