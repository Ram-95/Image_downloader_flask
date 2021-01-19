#Emails the downloaded and zipped gallery

import smtplib
import os
from email.message import EmailMessage
import imghdr

#Sender Credentials
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

def send_mail(filename, caption=""):
    '''Sends only .zip files. Else raises Exception.'''
    #Email Structure
    msg = EmailMessage()
    msg['Subject'] = filename + ' Gallery'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'ramm.y2k@gmail.com'
    msg.set_content(f'Hi,\n\nPlease find *** {filename} *** gallery in the attachment.\n<<{caption}>>\n\n\nThank you,\nPython Script')
    ext = '.zip'

    files = [filename + ext]

    print(f'\nSending Email... ')
    for file in files:
        '''Attaching the Images one by one'''
        #Reading an Image and getting its details
        with open(file, 'rb') as f:
            file_data = f.read()
            # Uncomment this when sending Images
            #file_type = imghdr.what(f.name)
            file_name = f.name

        #Adding the attachment to the Email message
        msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename= file_name)


    #Code for Sending Email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


    print('EMAIL SENT SUCCESSFULLY.')
