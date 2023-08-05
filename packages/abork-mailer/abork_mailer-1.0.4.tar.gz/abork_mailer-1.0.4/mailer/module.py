from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from tkinter import N
from typing import List
import smtplib
import os


class WrongParameterType(Exception):
    pass


class IMail:

    def send(self):
        raise NotImplementedError('Method "send" not implemented.')

    def add_attachment(self):
        raise NotImplementedError('Method "add_attachment" not implemented.')
  

class SmtpMail(IMail):

    def __init__(self, 
                    smtp_host: str = None, 
                    smtp_port: int = None, 
                    smtp_user: str = None, 
                    smtp_password: str = None,
                    mail_subject: str = None,
                    mail_recipients: list[str] = None,
                    mail_text: str = None,
                    mail_text_html: str = None):

        if not isinstance(mail_recipients, list):
            raise WrongParameterType('Recipients is not a list')

        for recipient in mail_recipients:
            if not isinstance(recipient, str):
                raise WrongParameterType('Not all of recipients are strings')
      
        self.host = smtp_host
        self.port = smtp_port
        self.user = smtp_user
        self.password = smtp_password
        self.sender = smtp_user
        self.recipients = mail_recipients
        self.subject = mail_subject
        self.text = mail_text
        self.text_html = mail_text_html
        self.attachments = []

    def add_attachment(self, file_path: str) -> None:

        if not file_path or not os.path.exists(file_path):
            raise ValueError('File does not exist.')

        attachment = {'file_path': file_path, 'file_name': os.path.basename(file_path)}
        self.attachments.append(attachment)

    def send(self) -> None:

        self.__check_data()
        self.__server_connect()
        mail = self.__build_mail()
        self.__add_attachments(mail)
        self.__send_mails(mail)
        self.__server_disconnect()

    def __add_attachments(self, mail: MIMEMultipart) -> None:

        for attachment in self.attachments:

            part = MIMEBase('application', 'octet-stream')

            with open(attachment['file_path'], "rb") as file:    
                part.set_payload(file.read())

            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=attachment['file_name'])
            
            mail.attach(part)

    def __send_mails(self, mail: MIMEMultipart) -> None:

        for recipient in self.recipients: 

            mail['To'] = recipient
            self.server.sendmail(self.sender, self.recipients, mail.as_string())

    def __server_disconnect(self) -> None:

        self.server.quit()

    def __server_connect(self) -> None:

        self.server = smtplib.SMTP(host=self.host, port=self.port)
        self.server.starttls()
        self.server.login(self.user, self.password)

    def __build_mail(self) -> MIMEMultipart:

        mail = MIMEMultipart()
        mail['From'] = self.sender
        mail['Subject'] = self.subject

        if self.text:
            mail.attach(MIMEText(self.text, 'plain'))
        else:
            mail.attach(MIMEText(self.text_html, "html"))

        return mail

    def __check_data(self) -> None:

        attrs_to_check = ['host', 'port', 'user', 'password', 'recipients', 'subject']
        msg_param = ''

        for attr in attrs_to_check:
            if not getattr(self, attr):
                msg_param += attr + ','

        if msg_param:
            msg_param = msg_param[0:len(msg_param)-1]
            raise ValueError(f'The following attributes have to be supplied: {msg_param}')

        if (not self.text and not self.text_html) or (self.text and self.text_html):
            raise ValueError('Supply either mail_text or mail_text_html')