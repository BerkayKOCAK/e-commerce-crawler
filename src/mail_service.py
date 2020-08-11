import smtplib
import logging

#Email Variables
SMTP_SERVER = 'smtp.gmail.com' #Email Server 
SMTP_PORT = 587 #Server Port 
GMAIL_USERNAME = 'raspberry.pi.berkay@gmail.com' 
GMAIL_PASSWORD = '.'  



class Emailer:
    async def sendmail(self, recipient, subject, content):
         
        try:
             #Create Headers
            headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                    "MIME-Version: 1.0", "Content-Type: text/plain; charset=utf-8"]
            headers = "\r\n".join(headers)
    
            #Connect to Gmail Server
            session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            session.ehlo()
            session.starttls()
            session.ehlo()
    
            #Login to Gmail
            session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    
            #Send Email & Exit
            session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
            session.quit

        except  Exception as identifier:
            logging.error("ERROR IN SEND-MAIL : "+str(identifier))
        
 


