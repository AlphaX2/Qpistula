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
            self.account.receive_mails()
        except:
            print "ERROR: NO CONNECTION, CHECK YOUR SETTINGS!"

    @QtCore.Slot()
    def refresh_mails(self):
        self.account.refresh_mails()

    @QtCore.Slot(int)
    def load_more_mails(self, last_count):
        #self.account.receive_mails(load_more=True, count=last_count)
        self.account.load_more_mails(last_count=last_count, add_new=50)

    def update_ui(self):
        print "update ui"
        self.mails_model = self.account.get_mails_model()
        qpistula.context.setContextProperty('mailListModel', self.mails_model)

    @QtCore.Slot(str, str, str, str, str, bool, str, str, str, bool)
    def save_server_settings(self, server_type='', mail_adress='',
                            inbox_user='', inbox_passwd='',
                            inbox_server='', inbox_use_ssl='',
                            outbox_user='', outbox_passwd='',
                            outbox_server='', outbox_use_ssl=''):

        self.account.save_server_settings(  server_type,
                                            mail_adress,
                                            inbox_user,
                                            inbox_passwd,
                                            inbox_server,
                                            inbox_use_ssl,
                                            outbox_user,
                                            outbox_passwd,
                                            outbox_server,
                                            outbox_use_ssl
                                            )

    @QtCore.Slot(result=str)
    def get_conf_for_gui(self):
        # Due to a PySide bug it's not possible to set result to a list, so just
        # give QML a string and split it via JavaScript in QML!
        conf_list = self.account.get_conf()
        conf_string =  ','.join(str(i) for i in conf_list)
        return conf_string

    @QtCore.Slot()
    def load_server_settings(self):
        self.account.read_conf()

    @QtCore.Slot(str, str, str)
    def send_mail(self, destination, subject, content):
        self.account.send_mail(destination, subject, content)

    @QtCore.Slot(int, int)
    def delete_mails(self, uid, index):
        # uid is for deleting the mail on the server, the index deletes the mail
        # from our own MailListModel
        self.account.delete_mails(uid, index)


#Starten der App
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    #create all needed instances before loading the UI
    mailing = MailActions()

    # create instance for the main application /application window
    qpistula = Qpistula()
    qpistula.view.show()

    sys.exit(app.exec_())
