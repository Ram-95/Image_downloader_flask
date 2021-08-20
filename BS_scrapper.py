'''Blogspot/tollywoodhq/s4all Image Scrapper and Downloader'''

import inspect
import bs4 as bs
import requests
import time
import concurrent.futures
import os
import string
import random
import shutil

class BS:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
        self.response = requests.get(self.url, self.headers)
        self.html = self.response.text
        self.soup = bs.BeautifulSoup(self.html, 'lxml')
        self.ext = '.jpg'
        #set base_url as 'tollywoodhq.com' if url is 'tollywoodhq' else '' [for blogspots]
        self.base_url = 'https://tollywoodhq.com' if 'tollywoodhq' in self.url else ''
        # If status_code is 200 then page exists. So it is a valid URL.
        if self.response.status_code == 200:
            self.invalid_url = False
        else:
            self.invalid_url = True
        self.img_urls = []
        self.main_dir = os.getcwd()
        self.caption = self.url.split('/')[-1][:-5].title()


    def create_random_directory(self):
        name = 'BST_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
        self.imgs_dir = os.path.join(self.main_dir, name)
        #Creating the new Directory
        os.mkdir(self.imgs_dir)
        print(f"\n'{name}' directory created")
        #Navigating to the newly created directory
        os.chdir(self.imgs_dir)

        return self.imgs_dir
        

    def get_img_urls(self):
        a = self.soup.findAll('a')
        for i in a:
            try:
                if i['href'].endswith('.jpg') or i['href'].endswith('.png'):
                    temp = i['href']
                    if temp.startswith('http'):
                        self.img_urls.append(self.base_url + temp)
                    else:
                        self.img_urls.append(self.base_url + temp)
            except Exception:
                continue
        #print(self.img_urls)
        if not self.img_urls:
            print(f'No Images in this site.')
        else:
            #print(f'Img_urls: {self.img_urls}')
            print(f'Image URLs captured.\n')



    def download(self):
        global count
        try:
            print(f'Downloading in progress... \n')
            for i in range(len(self.img_urls)):
                r = requests.get(self.img_urls[i], stream=True)
                with open(str(count+1)+ self.ext, 'wb') as outfile:
                    outfile.write(r.content)
                count += 1
        except Exception as e:
            raise e


    def zip_images(self, directory):
        try:
            '''Zips the contents of the Directory'''
            shutil.make_archive(directory, 'zip', directory)
            print(f'\nZip Successful.')
        except Exception as e:
            print(f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')


def download_images(img_url: str) -> None:
    title = img_url.split('/')[-1]
    r = requests.get(img_url, stream=True)
    with open(title, "wb") as outfile:
        outfile.write(r.content)


def start(url):
    global count
    count = 0
    start = time.perf_counter()
    base_dir = os.getcwd()

    if url.startswith('http://sumon4all.blogspot.com'):
        '''This logic is for s4all webpages'''
        bs = BS(url)
        if bs.invalid_url == False:
            # Create a directory
            imgs_dir = bs.create_random_directory()
            # Grab the page_urls 
            d = bs.soup.findAll('div', class_='separator')
            page_urls = d[1].findAll('a') if len(d) > 0 else []
            page_urls = [i['href'] for i in page_urls]
            page_urls.append(url)

            # Navigate to every page and download images
            for i in range(len(page_urls)):
                print(f'***** Page: {i+1} *****\n')
                bs = BS(page_urls[i])
                bs.get_img_urls()
                bs.download()
            print(f'\n******** {count} Images downloaded.********')
        else:
            print(f'\nInvalid URL.\n')
        
    else:
        '''This logic is for BS/THQ.'''
        # Creating a BS object
        bs = BS(url)

        if bs.invalid_url == False:
            bs.get_img_urls()
            # Continue only if the img_urls are captured.
            if bs.img_urls:
                imgs_dir = bs.create_random_directory()
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    executor.map(download_images, bs.img_urls)
                #bs.download()
                print(f'\n******** {len(bs.img_urls)} Images downloaded.********')
            else:
                bs.invalid_url = True
                return bs.invalid_url
    
        else:
            print(f'\nInvalid URL.\n')

    #Navigating back to the main directory
    os.chdir(base_dir)

    #Zip files
    bs.zip_images(os.path.basename(imgs_dir))
    print(f'\nCaption: {bs.caption}\n')

    # Deleting the gallery directory
    shutil.rmtree(imgs_dir)
    print(f'Main directory deleted: {imgs_dir}')
    finish = time.perf_counter()
    print(f'\nProcess completed in: {round(finish-start,2)} second(s).\n')
    return (bs.invalid_url, imgs_dir)