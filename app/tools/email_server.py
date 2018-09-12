# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging


class EmailServer(object):
    def __init__(self, server, port, user, password, tls=False):
        logging.debug("Connecting to email server...")
        self.__server = smtplib.SMTP(server, port)
        if tls:
            self.__server.starttls()
        self.__server.login(user, password)

    def __map_type(self, _type='text'):
        _type = _type.strip().lower()
        if _type == "html":
            return "html"
        if _type in ["text", "txt", "plain"]:
            return "plain"
        return _type


    def send_email(self, message, subject=None, _from=None, _to=None, _type='text'):
        msg = MIMEMultipart()
        _type = _type.lower()
        if _type in ["txt", "text"]:
            _type = "plain"
        
        msg["From"] = _from
        msg["To"] = _to
        msg["Subject"] = subject
        
        mime = MIMEText(message, self.__map_type(_type))
        msg.attach(mime)
        logging.debug("Sending email to %s ...", msg["To"])
        self.__server.sendmail(msg['From'], msg['To'], msg.as_string())

    def close(self):
        self.__server.quit()
