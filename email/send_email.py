# coding=utf-8

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import os.path
import smtplib

import ujson


class SendEmail(object):
    def __init__(self, host, port, user, password):
        self.sender = smtplib.SMTP(host, port)
        self.sender.starttls()  # put the SMTP connection in TLS(Transport Layer Security) mode
        self.sender.login(user, password)

    def run(self, from_addr, to_addrs, subject, text=None, files=None, cc=None):
        if not isinstance(to_addrs, list):
            to_addrs = [to_addrs]

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = COMMASPACE.join(to_addrs)
        if cc is not None:
            msg['Cc'] = COMMASPACE.join(cc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        if text is not None:
            msg.attach(MIMEText(text))

        if files is not None:
            if not isinstance(files, list):
                files = [files]

            for file_ in files:
                with open(file_, 'rb') as f:
                    payload = MIMEApplication(f.read(), Name=os.path.basename(file_))
                    payload['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file_)
                    msg.attach(payload)

        self.sender.sendmail(from_addr, to_addrs, msg.as_string())
        self.sender.quit()
