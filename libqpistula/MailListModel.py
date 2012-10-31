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

