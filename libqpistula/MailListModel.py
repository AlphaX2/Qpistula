from PySide import QtCore

class MailListModel(QtCore.QAbstractListModel):
    COLUMNS = ('mails',)

    def __init__(self, mails):
        QtCore.QAbstractListModel.__init__(self)
        self._mails = mails
        self.setRoleNames(dict(enumerate(MailListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._mails)

    def data(self, index, role):
        if index.isValid() and role == MailListModel.COLUMNS.index('mails'):
            return self._mails[index.row()]
        return None

    @QtCore.Slot(str, result=str)
    def get_sender(self, index):
        sender = self._mails[int(index)]._sender()
        sender = sender.split('<')
        sender = sender[1]
        sender = sender.replace('>', '')
        return sender

    @QtCore.Slot(str, result=str)
    def get_subject(self, index):
        return self._mails[int(index)]._subject()

    @QtCore.Slot(str, result=str)
    def get_message(self, index):
        return self._mails[int(index)]._message()

    @QtCore.Slot(str, result=str)
    def get_date(self, index):
        return self._mails[int(index)]._date()

    @QtCore.Slot(int, result=long)
    def get_uid(self, index):
        return self._mails[int(index)]._mailuid()

