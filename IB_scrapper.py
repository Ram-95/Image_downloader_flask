#Idlebrain - Scrapper
from Utilities import utilities
import time
import inspect
import shutil
import bs4 as bs
import requests
import random
import string
import os
import Email_send as email

class IB(utilities):
    def __init__(self, url):
        super().__init__()
        try:
            self.url = url
            self.caption = url.split('/')[-2].title()
            self.base = self.url[:-10]
            self.headers = {
                "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
            self.response = requests.get(self.url, self.headers)
            self.html = self.response.text
            self.soup = bs.BeautifulSoup(self.html, 'lxml')
            # flag to know if the provided URL exists or Not.
            # invalid_url = False [URL exists. Download Images]
            # invalid_url = True [URL Doesn't exist. Return]
            if self.response.status_code == 200:
                self.invalid_url = False
            else:
                self.invalid_url = True
        except Exception as e:
            print(f'***** EXCEPTION *****\n{e}')

    
    # More generic code - Works for both Old and New layout of galleries
    def __get_img_urls(self):
        try:
            b = self.soup.findAll('img')
            for i in b:
                temp = i['src']
                try:
                    if 'th_' in temp:
                        # Logic for new galleries
                        temp = temp.replace('th_', '')
                        # To remove IB logo image from appending to the img_urls
                        if '.gif' not in temp:
                            self.img_urls.append(self.base + temp)

                    elif 'thumb' in temp:
                        # Logic for old galleries
                        temp = temp.replace('thumb', 'newpg')
                        if '../../' in temp:
                            temp = temp.replace(
                                '../../', 'http://www.idlebrain.com/')
                            self.img_urls.append(temp)
                except:
                    pass
            print(f'\nImages URLs captured.')
        except Exception as e:
            print(
                f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')


    def start(self):
        if self.invalid_url == False:
            dir_name = super().create_random_directory('IB')
            self.__get_img_urls()
            super().download()
            if not os.listdir():
                # Deleting the imgs_directory if empty
                os.chdir(self.main_dir)
                os.rmdir(self.imgs_dir)
                self.invalid_url = True
                print('Empty Directory deleted.')
                return (self.invalid_url, dir_name)
            
            # Navigating back to the main directory
            os.chdir(self.main_dir)
            super().zip_images(dir_name)
            
            # Emailing the file
            super().send_mail(dir_name, self.caption)
            
            # Deleting the uncompressed directory after zipping
            super().delete_dir(dir_name)
        else:
            print('Invalid URL')
        return (self.invalid_url, dir_name)
