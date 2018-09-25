# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate
import smtplib
import logging
from encode import ustr, encode_header, encode_rfc2822_address_header
import time
import random
import os
import socket


class EmailServer(object):
    def __init__(self, server, port, user, password, encoding=False):
        logging.debug("Connecting to email server...")

        if encoding:
            encoding = encoding.lower().strip()

        port = int(port)
        if encoding == "ssl" and 'SMTP_SSL' in smtplib.__all__:
            self.__server = smtplib.SMTP_SSL(server, port)
        else:
            self.__server = smtplib.SMTP(server, port)

        if encoding == "tls":
            self.__server.starttls()

        self.__server.ehlo()
        user = ustr(user).encode('utf-8')
        password = ustr(password).encode('utf-8')

        self.__server.login(user, password)
        self.__user = user

    def __map_type(self, _type='text'):
        _type = _type.strip().lower()
        if _type == "html":
            return "html"
        if _type in ["text", "txt", "plain"]:
            return "plain"
        return _type

    def build_email(self, message, subject=None, _to=None, _type='text'):
        logging.debug("Building email to %s ...")
        _type = _type.lower()
        if _type in ["txt", "text"]:
            _type = "plain"

        msg = MIMEMultipart()

        msg["Message-Id"] = encode_header(make_msgid())
        msg["From"] = encode_rfc2822_address_header(self.__user)
        msg["To"] = encode_rfc2822_address_header(_to)
        msg["Subject"] = encode_header(subject)
        msg['Date'] = formatdate()

        message_utf8 = ustr(message).encode('utf-8')
        mime_text = MIMEText(message_utf8, _subtype=self.__map_type(_type), _charset='utf-8')
        msg.attach(mime_text)
        return msg

    def send_email(self, message, subject=None, _to=None, _type='text'):
        msg = self.build_email(message, subject=subject, _to=_to, _type=_type)
        logging.debug("Sending email to %s ...", msg["To"])
        self.__server.sendmail(self.__user, msg['To'].split(", "), msg.as_string())

    def close(self):
        self.__server.quit()
