#-*- coding: utf-8 -*-

import os
import pickle

from PySide import QtCore
from imapclient import IMAPClient

from MailWrapper import MailWrapper
from MailListModel import MailListModel

__SETTINGS_PATH__ = '/home/gabriel/Programmieren/Python/Eigene/Qpistula/devel/qpistula_login.cfg'

class MailAccount(QtCore.QObject):
    ''' holds account data and manage mail actions'''
    def __init__(self):
        QtCore.QObject.__init__(self)

        self.settings = {
                    'inbox_server_type': None, # NOT IN USE, later maybe pop/imap
                    'inbox_username': '',
                    'inbox_password': '',
                    'inbox_server': '',
                    'inbox_use_ssl': False
                    }

        self.signal = Signal()
        self.first_mail_msg = None
        self.mails_model = None

    def load_inbox_server_settings(self):
        '''
        Loads your account settings from settings file.
        '''
        try:
            with open(__SETTINGS_PATH__) as cfg:
                self.settings = pickle.load(cfg)
                print self.settings
        except:
            print "ERROR: COULD NOT LOAD SETTINGS"

    def save_inbox_server_settings(self, server_type='', user='', passwd='', server='', ssl=''):

        # NOT IMPLEMENTED AT THE MOMENT, JUST FOR SETTING POP/IMAP LATER!
        self.settings['inbox_server_type'] = server_type

        self.settings['inbox_username'] = user
        self.settings['inbox_password'] = passwd
        self.settings['inbox_server']   = server
        self.settings['inbox_use_ssl']  = ssl

        #TODO: filename related to the account name, first of all implement the different accounts
        with open(__SETTINGS_PATH__, 'w') as cfg:
            pickle.dump(self.settings, cfg)

    def receive_mails(self, folder='INBOX'):
        '''
        Call this function to start the MailCheckThread receiving latest mails.
        And connect the receivingFinished signal to update your UI!
        '''
        self.mail_check = MailCheckThread(  self.settings["inbox_username"],
                                            self.settings["inbox_password"],
                                            self.settings["inbox_server"],
                                            self.settings["inbox_use_ssl"])
        # create from server response a Qt/QML friendly model
        self.mail_check.finished.connect(self._create_mail_model)
        self.mails = self.mail_check.start(folder=folder)

    # When MailCheckThread finished this function creates a Qt/QML model
    def _create_mail_model(self):
        response = self.mail_check.response
        mails = [MailWrapper(response[id]['RFC822']) for id in reversed(response.keys())]
        self.mails_model = MailListModel(mails)

        # getting text from lattest mail
        length = len(response)
        first_mail = MailWrapper(response[length]['RFC822'])
        self.first_mail_msg = first_mail._message()
        print self.first_mail_msg

        self.signal.receiving_done.emit()


    def get_mails_model(self):
        return self.mails_model


    def get_first_mail_msg(self):
        return self.first_mail_msg


    def delete_mails(self, uids):
        pass


    def search(self):
        pass


class MailCheckThread(QtCore.QThread):
    def __init__(self, user, passwd, imap_server, use_ssl):
        QtCore.QThread.__init__(self)
        self.server = IMAPClient(imap_server, use_uid=True, ssl=use_ssl)
        self.user = user
        self.passwd = passwd
        self.response = {}
        self.server.login(self.user, self.passwd)


    def run(self, folder='INBOX'):
        self.server.select_folder(folder)
        self.response = self.server.fetch('1:*', ['RFC822'])


class Signal(QtCore.QObject):
    ''' own signals '''
    receiving_done = QtCore.Signal()
