# Image_Downloader_Flask

A web app to scrape and download images from these websites - Idlebrain, Ragalahari, Cinejosh and Blogspot/sumon4all/tollywoodhq.com galleries.

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
        
        :: Setting DEBUG as True/False. Always set to 'True' in Dev environment and 'False' in Prod environment.
        set FLASK_DEBUG=True
        
        ::Starting the flask server
        flask run
        
        PAUSE

#### Given a gallery URL, this site will
 - Create a directory.
 - Download the images from the URL and saves it to the directory.
 - Zip the directory and provides the zip folder as download attachment.
