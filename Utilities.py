''' Common Utilities used by all the scrapper scripts.'''
import time
import inspect
import shutil
import requests
import random
import string
import os
import Email_send as email


class utilities:
    def __init__(self):
        self.ext = '.jpg'
        self.main_dir = 'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python38-32\\IB_downloader_flask\\'
        #self.curr_dir = os.getcwd() + '\\'
        self.imgs_dir = ''
        self.img_urls = []

    def create_random_directory(self, prefix):
        try:
            # Generates a random name
            name = prefix + '_' + \
                ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=6))
            # Creating the Directory
            self.imgs_dir = self.main_dir + name
            os.mkdir(self.imgs_dir)
            print(f"\n'{self.imgs_dir}' directory created.")
            # Navigating to the newly created Directory
            os.chdir(self.imgs_dir)
        except Exception as e:
            raise Exception(
                f'***** EXCEPTION in "{inspect.stack()[0].function}()" *****\n{e}')
        return os.path.basename(self.imgs_dir)

    def download(self):
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

    def zip_images(self, directory):
        os.chdir(self.main_dir)
        try:
            '''Zips the contents of the Directory'''
            print(f'\n\nDirectory: {directory}\n\n')
            shutil.make_archive(directory, 'zip', directory)
            print(f'\nZip Successful.')
        except Exception as e:
            raise e

    def send_mail(self, directory, caption="Gallery"):
        try:
            email.send_mail(directory, caption)
        except Exception as e:
            raise Exception(e)

    def delete_dir(self, directory):
        # Deleting the uncompressed directory after zipping
        shutil.rmtree(directory)
        print(f'\nMain Directory deleted. <{directory}>\n')
