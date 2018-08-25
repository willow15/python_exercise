# coding=utf-8

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
import smtplib
from zipfile import ZipFile


class SendZippedFile(object):
    def __init__(self, host, port, user, password):
        self.sender = smtplib.SMTP(host, port)
        self.sender.starttls()
        self.sender.login(user, password)

    def run(self, from_addr, to_addrs, subject, files):
        if not isinstance(to_addrs, list):
            to_addrs = [to_addrs]

        if not isinstance(files, list):
            files = [files]

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = COMMASPACE.join(to_addrs)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        zf = 'template.zip'
        with ZipFile(zf, 'w') as myzip:
            for f in files:
                myzip.write(f)

        payload = MIMEBase(_maintype='application', _subtype='zip')
        with open(zf, 'rb') as myzip:
            payload.set_payload(myzip.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename='template.zip')
        msg.attach(payload)

        self.sender.sendmail(from_addr, to_addrs, msg.as_string())
        self.sender.quit()
