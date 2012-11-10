#-*- coding: utf-8 -*-

from PySide import QtCore
import email
from email.header import decode_header
from email.iterators import body_line_iterator, _structure

class MailWrapper(QtCore.QObject):
    def __init__(self, uid, mail):
        QtCore.QObject.__init__(self)
        self._uid = uid
        self._mail = email.message_from_string(mail)

    def _sender(self):
        sender = ' '.join([part[0] for part in decode_header(self._mail['from'])])
        return unicode(sender.replace('\r',''))  
       
    def _subject(self):
        print decode_header(self._mail['subject'])
        charset = decode_header(self._mail['subject'])[0][1]
        if charset:
            return unicode(' '.join([part[0] for 
                           part in decode_header(self._mail['subject'])]),charset)
        else:
            return ' '.join([part[0] for 
                           part in decode_header(self._mail['subject'])])

    def extract_message(self):
        if self._mail.is_multipart():
            msg = []
            for part in self._mail.walk():
                # each part is a either non-multipart, or another multipart message
                # that contains further parts... Message is organized like a tree
                if part.get_content_type() in ['text/html']:
                    msg.append(part.get_payload(decode=True))
            return u' '.join([part for part in msg])
        else:
            charset = self._mail['Content-Type'].replace('\r\n\t',' ').split('; charset=')[1]
            charset = charset.lower().replace('"','')
            print charset
            return unicode(self._mail.get_payload(decode=True).replace('\r',''), charset)
            # QML Text Elements don't know '\r', so remove it
         
    def _preview(self):
        return self.extract_message()[:150]

    def _mailuid(self):
        return self._uid

    def _message(self):
        return self.extract_message()

    def _date(self):
        return self._mail['date']

    changed = QtCore.Signal()

    sender = QtCore.Property(unicode, _sender, notify=changed)
    subject = QtCore.Property(unicode, _subject, notify=changed)
    preview = QtCore.Property(unicode, _preview, notify=changed)
    date = QtCore.Property(unicode, _date, notify=changed)
    message = QtCore.Property(unicode, _message, notify=changed)
    uid = QtCore.Property(int, _mailuid, notify=changed)

