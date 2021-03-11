# Image_Downloader_Flask

A flask app to scrape and download images from websites like - Idlebrain, Ragalahari, Cinejosh and Blogspot/sumon4all/tollywoodhq.com galleries.

### Steps to run the application
  - Install all the dependencies from ```requirements.txt```.
  - Open command prompt in the projects directory and write the following commands
    - ```set FLASK_APP = main.py``` - This will tell Flask to point the application to ```main.py```.
    - ```set FLASK_DEBUG = True``` - This will tell Flask to set the debug option to ```True```. We can know the errors of our application only if ```DEBUG=True```.
  - Type ```flask run``` command to start the application.
  
  - **Alternatively you could put the above commands in a Windows batch file(_see below_) and just run it to start the application.**
    ```ECHO OFF
        :: Setting the FLASK_APP to main.py
        set FLASK_APP=main.py
        
        :: Setting DEBUG as True/False. Always set to 'True' in Dev environment and 'False' in Prod.
        set FLASK_DEBUG=True
        
        ::Starting the flask server
        flask run
        
        PAUSE```

#### All the images will be saved to a directory, will be zipped and available for download.
