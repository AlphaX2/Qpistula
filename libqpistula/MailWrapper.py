#-*- coding: utf-8 -*-

from PySide import QtCore
import email
from email.header import decode_header

class MailWrapper(QtCore.QObject):
    def __init__(self, uid, mail):
        QtCore.QObject.__init__(self)
        self._uid = uid
        self._mail = email.message_from_string(mail)

    def _sender(self):
        return ' '.join([part[0] for part in decode_header(self._mail['from'])]) 
        #sender = []
        #for part, charset in decode_header(self._mail['from']):
        #   if charset:
        #       sender.append(part.decode(charset))
        #   else:
        #       sender.append(part)
        #return ' '.join(sender)   
       
    def _subject(self):
        return ' '.join([part[0] for part in decode_header(self._mail['subject'])])   
        #return self.getheader(self._mail['subject'])

    def extract_message(self):
        if self._mail.is_multipart():
            return ""
        else:
            return unicode(self._mail.get_payload(decode=True).replace('\r',''))
         
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

