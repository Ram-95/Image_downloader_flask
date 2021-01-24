'''Blogspot/tollywoodhq/s4all Image Scrapper and Downloader. '''

import inspect
import bs4 as bs
import requests
import urllib.request
import os
import string
import random
import shutil
import Email_send as email

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
        self.main_dir = os.getcwd() + '\\'
        self.mail_send = False
        self.caption = self.url.split('/')[-1][:-5].title()


    def create_random_directory(self):
        name = 'BST_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
        self.imgs_dir = self.main_dir + name
        #Creating the new Directory
        os.mkdir(self.imgs_dir)
        print(f"\n'{name}' directory created")
        #Navigating to the newly created directory
        os.chdir(self.imgs_dir)


    def get_img_urls(self):
        a = self.soup.findAll('a')
        for i in a:
            try:
                if i['href'].endswith('.jpg'):
                    self.img_urls.append(self.base_url + i['href'])
            except Exception:
                continue
        #print(self.img_urls)
        if not self.img_urls:
            print(f'No Images in this site.')
        else:
            print(f'\nImage URLs captured.')



    def download(self):
        try:
            print(f'\nDownloading in progress...\n')
            for i in range(len(self.img_urls)):
                r = requests.get(self.img_urls[i], stream=True)
                with open(str(i+1)+ self.ext, 'wb') as outfile:
                    outfile.write(r.content)
            
            print(f'\n******** {len(self.img_urls)} Images downloaded.********')
        except Exception as e:
            raise e


    def zip_images(self, directory):
        try:
            '''Zips the contents of the Directory'''
            shutil.make_archive(directory, 'zip', directory)
            print(f'\nZip Successful.')
        except Exception as e:
            print(f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')


    def send_mail(self, directory):
        try:
            email.send_mail(directory, self.caption)
        except Exception as e:
            raise Exception(e)


def start(url):
    # Creating a BS object
    bs = BS(url)
    if bs.invalid_url == False:
        bs.get_img_urls()
        # Continue only if the img_urls are captured.
        if bs.img_urls:
            bs.create_random_directory()
            bs.download()
            
            #Navigating back to the main directory
            os.chdir(bs.main_dir)

            # Zip files
            bs.zip_images(os.path.basename(bs.imgs_dir))
            print(f'\nCaption: {bs.caption}\n')

            # Deleting the gallery directory
            shutil.rmtree(bs.imgs_dir)
            print(f'Main directory deleted: {bs.imgs_dir}')
            
            # Email the files
            if bs.mail_send:
                bs.send_mail(os.path.basename(bs.imgs_dir))
            else:
                print("\n'mail_send' flag is set to False. Email not sent.\n")
        else:
            bs.invalid_url = True
            return bs.invalid_url
    else:
        print(f'\nInvalid URL.\n')
    
    return bs.invalid_url

