from PySide import QtCore
import email
import chardet

class MailWrapper(QtCore.QObject):
    def __init__(self, uid, mail):
        QtCore.QObject.__init__(self)
        self._uid = uid
        self._mail = email.message_from_string(mail)

    def _sender(self):
        return self._mail['from'].decode("utf-8")
 
    def _subject(self):
        return self._mail['subject'].decode("utf-8")

    def _preview(self):
        return self.extract_message()[:150].decode("utf-8")

    def _mailuid(self):
        return self._uid

    def _message(self):
        return self.extract_message().decode("utf-8")

    def extract_message(self):
        text = ""
        msg = self._mail
        if msg.is_multipart():
            html = True #None
            for part in msg.get_payload():
                if part.get_content_charset() is None:
                    charset = chardet.detect(str(part))['encoding']
                else:
                    charset = part.get_content_charset()
                if part.get_content_type() == 'text/plain':
                    text = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
                if part.get_content_type() == 'text/html':
                    html = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
            if html is None:
                return text.strip()
            else:
                return html.strip()
        else:
            return msg.get_payload().decode("utf-8")

    def _date(self):
        return self._mail['date']

    changed = QtCore.Signal()

    sender = QtCore.Property(unicode, _sender, notify=changed)
    subject = QtCore.Property(unicode, _subject, notify=changed)
    preview = QtCore.Property(unicode, _preview, notify=changed)
    date = QtCore.Property(unicode, _date, notify=changed)
    message = QtCore.Property(unicode, _message, notify=changed)
    uid = QtCore.Property(int, _mailuid, notify=changed)

