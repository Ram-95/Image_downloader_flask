'''Idlebrain - Scrapper'''

import time
import inspect
import shutil
import bs4 as bs
import requests
import random
import string
import os
import Email_send as email


class IB:
    def __init__(self, url):
        try:
            self.url = url.split('#')[0]
            self.caption = url.split('/')[-2].title()
            self.base = self.url[:-10]
            self.headers = {
                "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
            self.response = requests.get(self.url, self.headers)
            self.html = self.response.text
            self.soup = bs.BeautifulSoup(self.html, 'lxml')
            self.ext = '.jpg'
            self.main_dir = os.getcwd()
            self.imgs_dir = self.main_dir
            self.img_urls = []
            # flag to know if the provided URL exists or Not.
            # invalid_url = False [URL exists. Download Images]
            # invalid_url = True [URL Doesn't exist. Return]
            if self.response.status_code == 200:
                self.invalid_url = False
            else:
                self.invalid_url = True
        except Exception as e:
            print(f'***** EXCEPTION *****\n{e}')

    def __create_random_directory(self):
        try:
            # Generates a random name
            name = 'IB_' + \
                ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=6))
            # Creating the Directory
            self.imgs_dir = os.path.join(self.main_dir, name)
            os.mkdir(self.imgs_dir)
            print(f"\n'{name}' directory created.")
            # Navigating to the newly created Directory
            os.chdir(self.imgs_dir)
        except Exception as e:
            raise Exception(
                f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')

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

    def __download(self):
        try:
            print(f'\nDownloading in progress...\n')
            for i in range(len(self.img_urls)):
                r = requests.get(self.img_urls[i], stream=True)
                with open(str(i+1) + self.ext, 'wb') as outfile:
                    outfile.write(r.content)

            print(
                f'\n******** {len(self.img_urls)} Images downloaded.********')
        except Exception as e:
            print(
                f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')

    def __zip_images(self, directory):
        try:
            '''Zips the contents of the Directory'''
            directory = os.path.basename(directory)
            shutil.make_archive(directory, 'zip', directory)
            print(f'\nZip Successful.')
        except Exception as e:
            print(
                f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')

    def __send_mail(self, directory):
        try:
            email.send_mail(directory, self.caption)
        except Exception as e:
            raise Exception(e)

    def start(self):
        if self.invalid_url == False:
            self.__create_random_directory()
            self.__get_img_urls()
            self.__download()
            if not os.listdir():
                # Deleting the imgs_directory if empty
                os.chdir(self.main_dir)
                os.rmdir(self.imgs_dir)
                self.invalid_url = True
                print('Empty Directory deleted.')
                return self.invalid_url
            # Navigating back to the main directory
            os.chdir(self.main_dir)
            self.__zip_images(os.path.basename(self.imgs_dir))
            
            # Emaling the file
            self.__send_mail(self.imgs_dir)
            
            # Deleting the uncompressed directory after zipping
            shutil.rmtree(self.imgs_dir)
            print(f'\nMain Directory deleted. <{self.imgs_dir}>\n')
        else:
            print('Invalid URL')
            return self.invalid_url


# Driver Code
'''
url = ''
i = IB(url)
i.start()

'''
