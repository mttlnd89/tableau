import smtplib
from smtplib import SMTPException
from email.message import EmailMessage
import yaml

class Email:
    def emailMessage(_message, _subject):
        with open('secrets.yml', 'r') as file:
            stuff = yaml.safe_load(file)
        try:
            msg = EmailMessage()
            msg['Subject'] = _subject
            msg['From'] = stuff['gmailuser']
            msg['To'] = stuff['gmailuser']
            msg.set_content(_message)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(stuff['gmailuser'],stuff['gmailapppassword'])
            s.send_message(msg)
            print('Email sent')
            s.quit()
        except SMTPException:
            print('Error: unable to send email')