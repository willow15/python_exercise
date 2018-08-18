# coding=utf-8

import base64
import email
import email.header
import imaplib
import os
import quopri


class DownloadAttachments(object):
    def __init__(self, host, port, user, password, attachments_dir):
        self.attachments_dir = attachments_dir
        self.m = imaplib.IMAP4_SSL(host, port)
        self.m.login(user, password)
        # code, mailboxes = self.m.list()
        # print mailboxes

    def run(self, from_someone, on_date):
        code, data = self.m.select(mailbox='INBOX', readonly=True)
        if code == 'OK':
            print 'start processing mailbox'
            self.download_attachments(from_someone, on_date)
            self.m.close()  # close currently selected mailbox
        else:
            print 'ERROR: unable to open mailbox'
        self.m.logout()

    def download_attachments(self, from_someone, on_date):
        search_keyword = '(FROM "' + from_someone + '" ON ' + on_date + ')'  # e.g. '(FROM "willow15" ON 18-Aug-2018)'
        code, msgnums = self.m.search(None, search_keyword)
        if code != 'OK':
            print 'ERROR: no messages found'
            return
        msgnums = msgnums[0].split()
        for msgnum in msgnums:
            code, data = self.m.fetch(msgnum, '(RFC822)')
            if code != 'OK':
                print 'ERROR: unable to get message', msgnum
                continue

            msg = email.message_from_string(data[0][1])
            subject = email.header.decode_header(msg['Subject'])[0][0]
            print 'subject:', subject

            content_type = msg.get_content_maintype()
            if content_type != 'multipart':
                print 'ERROR: mail type', content_type
            else:
                for part in msg.walk():
                    if part.get('Content-Disposition') is not None:
                        filename = part.get_filename()
                        if '?' in filename:
                            info = filename.split('?')  # =?<charset>?<encoding>?<data>?=
                            charset = info[1]
                            encoding = info[2]
                            data = info[3]
                            if encoding == 'B':
                                filename = base64.b64decode(data).decode(charset)
                            elif encoding == 'Q':
                                filename = quopri.decodestring(data).decode(charset)
                        print 'filename:', filename
                        if filename.endswith(('docx', 'csv', 'xlsx', 'gif', 'jpg', 'pdf')):
                            file_path = os.path.join(self.attachments_dir, filename)
                            if not os.path.isfile(file_path):
                                with open(file_path, 'wb') as f:
                                    f.write(part.get_payload(decode=True))
                            else:
                                file_path = os.path.join(self.attachments_dir, 'duplicate_' + filename)
                                with open(file_path, 'wb') as f:
                                    f.write(part.get_payload(decode=True))
