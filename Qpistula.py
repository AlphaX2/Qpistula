#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import pickle
import imaplib
from PySide import QtGui, QtDeclarative, QtCore
from libqpistula.MailWrapper import MailWrapper
from libqpistula.MailListModel import MailListModel
from libqpistula.Account import MailAccount

#QtOpenGL
reload(sys)
sys.setdefaultencoding('utf-8')

#__SETTINGS_PATH__ = '/home/gabriel/Programmieren/Python/Eigene/Qpistula/devel/qpistula_login.cfg'

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

        self.mails_model = None
        self.account = MailAccount()
        self.account.signal.receiving_done.connect(self.update_ui)

        try:
            #self.account.load_inbox_server_settings()
            self.account.receive_mails()
        except:
            print "ERROR: NO CONNECTION, CHECK YOUR SETTINGS!"

    @QtCore.Slot()
    def refresh_mails(self):
        self.account.receive_mails()

    def update_ui(self):
        self.mails_model = self.account.get_mails_model()
        qpistula.context.setContextProperty('mailListModel', self.mails_model)

    @QtCore.Slot(str, str, str, str, bool)
    def save_inbox_server_settings(self, server_type='', user='', passwd='', server='', ssl=''):
        self.account.save_inbox_server_settings(server_type, user, passwd, server, ssl)

    @QtCore.Slot()
    def load_inbox_server_settings(self):
        self.account.load_inbox_server_settings()

    @QtCore.Slot(str, str, str)
    def send_mail(self, destination, subject, content):
        self.account.send_mail(destination, subject, content)

    @QtCore.Slot(int)
    def delete_mails(self, uid):
        print "delete_mails (Qpistula.py):"
        print "uid: "+str(uid)
        self.account.delete_mails(uid)


#Starten der App
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    #create all needed instances before loading the UI
    mailing = MailActions()

    # create instance for the main application /application window
    qpistula = Qpistula()
    qpistula.view.show()

    sys.exit(app.exec_())
