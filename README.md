# Image_Downloader_Flask

A flask app to scrape and download images from websites like - Idlebrain, Ragalahari, Cinejosh and Blogspot/sumon4all/tollywoodhq.com galleries.

### Steps for first time use
  - Install all the dependencies from ```requirements.txt```.
  - Open command prompt in the projects directory and write the following commands
    - ```set FLASK_APP = main.py``` - This will tell Flask to point the application to ```main.py```.
    - ```set FLASK_DEBUG = True``` - This will tell Flask to set the debug option to ```True```. We can know the errors of our application only if ```DEBUG=True```.
  - Type ```flask run``` command to start the application.

#### All the images will be saved to a directory, will be zipped and available for download.