#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import imaplib
from PySide import QtGui, QtDeclarative, QtCore
from libqpistula.MailWrapper import MailWrapper
from libqpistula.MailListModel import MailListModel
from libqpistula.Account import MailAccount

#QtOpenGL
reload(sys)
sys.setdefaultencoding('utf-8')

__SETTINGS_PATH__ = '/home/gabriel/Programmieren/Python/Eigene/Qpistula/devel/qpistula_login.cfg'

class Qpistula(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        #OpenGL Rendering
        #self.glw = QtOpenGL.QGLWidget()
        #self.view.setViewport(self.glw)

        self.view = QtDeclarative.QDeclarativeView()
        self.view.setResizeMode(self.view.SizeRootObjectToView)

        self.context = self.view.rootContext()
        self.context.setContextProperty('mail', mailing)
        self.view.setSource('qml/main.qml')

class MailActions(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        # Holds the first msg text for showing it at startup!
        self.first_msg = None
        self.mails_model = None
        self.account = MailAccount(__SETTINGS_PATH__)
        self.account.receive_mails()
        self.account.signal.receiving_done.connect(self.update_ui)

    @QtCore.Slot()
    def refresh_mails(self):
        self.account.receive_mails()

    def update_ui(self):
        self.first_msg = self.account.get_first_mail_msg()
        self.mails_model = self.account.get_mails_model()
        qpistula.context.setContextProperty('mailListModel', self.mails_model)

    # Ask for self.first_msg from QML!
    @QtCore.Slot(result=unicode)
    def show_first_message(self):
        return self.first_msg

#Starten der App
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    #create all needed instances before loading the UI
    mailing = MailActions()

    # create instance for the main application /application window
    qpistula = Qpistula()
    qpistula.view.show()

    sys.exit(app.exec_())
