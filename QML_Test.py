#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import imaplib
from PySide import QtGui, QtDeclarative, QtCore
from MailWrapper import MailWrapper
from MailListModel import MailListModel
from Account import MailAccount
#QtOpenGL
reload(sys)
sys.setdefaultencoding('utf-8')

class Qpistula(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.view = QtDeclarative.QDeclarativeView()
        #OpenGL Rendering
        #self.glw = QtOpenGL.QGLWidget()
        #self.view.setViewport(self.glw)
        self.view.setSource('qml/main.qml')
        self.root = self.view.rootObject()
        self.context = self.view.rootContext()

#        self.root.refresh_mails.connect(self.refresh_mails)

#        # alte version zum testen
#        #self.mail_account = imaplib.IMAP4('imap.pohlers-web.de')
#        #self.mail_account.login('m026c248', '7UD9gJZVqSe95zpY')
#        #self.mail_account.select()
#        #typ, data = self.mail_account.search(None, 'ALL')
#        #self.mails = []
#        #for num in data[0].split()[-30:]:
#        #     typ, data = self.mail_account.fetch(num, '(RFC822)')
#        #     #print 'Message %s\n%s\n' % (num, data[0][1])
#        #     #print type(data[0][1])
#        #     self.mails.append(data[0][1])
#        
#        self.mails = {}
#        self.account = MailAccount()
#        self.account.check_mails()
#        self.account.signal.loading_done.connect(self.update_ui)

#    def refresh_mails(self):
#        self.account.check_mails()

#    def update_ui(self,mails):
#        #print mails
#        self.mails = [MailWrapper(mails[id]['RFC822']) for id in reversed(mails.keys())]
#        self.mails_model = MailListModel(self.mails)
#        self.context.setContextProperty('mailListModel', self.mails_model)


#Starten der App
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    qpistula = Qpistula()
    qpistula.view.show()
    sys.exit(app.exec_())
