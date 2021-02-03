#Emails the downloaded and zipped gallery

import smtplib
import os
from email.message import EmailMessage
import imghdr

#Sender Credentials
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
# Flag to set whether to send email or not.
mail_send = False

def send_mail(filename, caption=""):
    '''Sends only .zip files. Else raises Exception.'''
    if mail_send:
        recipient = 'ramm.y2k@gmail.com'
        #Email Structure
        msg = EmailMessage()
        filename = os.path.basename(filename)
        msg['Subject'] = filename + ' Gallery'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg.set_content(f'Hi,\n\nPlease find *** {filename} *** gallery in the attachment.\n<<{caption}>>\n\n\nThank you,\nPython Script')
        ext = '.zip'
        
        files = [filename + ext]

        '''Send Mail only if the size of zip file is less than 25 MB.'''
        MB = int(1e6)
        print(files[0])
        size = round(os.path.getsize(files[0])/MB)
        print(f'\nSize is: {size} MB (approx)')
        if size in range(1, 25):
            print(f'\nSending Email... \n')
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
            

            print(f'EMAIL SENT SUCCESSFULLY to "{recipient}"')
        else:
            print('Your attachment size is greater than 25MB. Not sending Email.')
    else:
        print(f"\n'mail_send' flag is set to False. Not sending email.\n")
    
    return


    
