#-*- coding: utf-8 -*-

import os
import pickle

from PySide import QtCore
from imapclient import IMAPClient

from MailWrapper import MailWrapper
from MailListModel import MailListModel

__SETTINGS_PATH__ = '/home/pohlerb/qpistula_login.cfg'

class MailAccount(QtCore.QObject):
    ''' holds account data and manage mail actions'''
    def __init__(self):
        QtCore.QObject.__init__(self)

        self.settings = {
                    'inbox_server_type': None, # NOT IN USE, later maybe pop/imap
                    'mail-adress': '',
                    'inbox_username': '',
                    'inbox_password': '',
                    'inbox_server': '',
                    'inbox_use_ssl': False,
                    'smtp_server': '',
                    'smtp_username': '',
                    'smtp_password': '',
                    'smtp_use_ssl': False
                    }

        self.signal = Signal()
        self.mails_model = None
        self.mail_check = None
        self.mail_search = None

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

    def save_inbox_server_settings(self, server_type='', mail_adress='', user='', passwd='', server='', ssl='',smtp_server= '', smtp_username='', smtp_password= '', smtp_use_ssl = False):

        # NOT IMPLEMENTED AT THE MOMENT, JUST FOR SETTING POP/IMAP LATER!
        self.settings['inbox_server_type'] = server_type

        self.settings['mail_adress'] = mail_adress
        self.settings['inbox_username'] = user
        self.settings['inbox_password'] = passwd
        self.settings['inbox_server']   = server
        self.settings['inbox_use_ssl']  = ssl
        self.settings['smtp_username']  = smtp_username
        self.settings['smtp_password']  = smtp_password
        self.settings['smtp_server']  = smtp_server
        self.settings['smtp_use_ssl']  = smtp_use_ssl

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
        mails = [MailWrapper(id,response[id]['RFC822']) for id in reversed(response.keys())]
        self.mails_model = MailListModel(mails)
        self.signal.receiving_done.emit()

    def send_mail(self, destination, subject, content):
        # the accounts mail adress
        sender=self.settings['mail_adress']
        destination = destination.split(",") # get multiple mails adresses

        # typical values for text_subtype are plain, html, xml
        text_subtype = 'html' #'plain'

        if self.settings['smtp_use_ssl']:
            # this invokes the secure SMTP protocol (port 465, uses SSL)
            from smtplib import SMTP_SSL as SMTP
        else:
            # use this for standard SMTP protocol (port 25, no encryption)
            from smtplib import SMTP
        from email.MIMEText import MIMEText

        try:
            msg = MIMEText(content.encode('utf-8'), text_subtype, 'UTF-8')
            msg['Subject']= subject
            msg['From']   = self.settings['mail_adress']
            msg['To'] = ','.join(destination)

            conn = SMTP(self.settings['smtp_server'])
            conn.set_debuglevel(False)
            conn.login(self.settings['smtp_username'],self.settings['smtp_password'])
            try:
                conn.sendmail(sender, destination, msg.as_string())
            finally:
                conn.close()
        except Exception, exc:
            sys.exit( "mail failed; %s" % str(exc) ) # give a error message

    def get_mails_model(self):
        return self.mails_model

    def delete_mails(self, uids):
        pass

    def delete_mails(self, index): #TODO: ADD SEARCH PHRASE(S)
        self.mail_delete = MailDeleteThread(self.settings['inbox_username'],
                                            self.settings['inbox_password'],
                                            self.settings['inbox_server'],
                                            self.settings['inbox_use_ssl'],
                                            index
                                            )
        self.mail_delete.finished.connect(self.receive_mails)
        self.mail_delete.start()

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
        # just show not deleted messages in the INBOX!
        messages = self.server.search(['NOT DELETED'])
        self.response = self.server.fetch(messages, ['RFC822'])


class MailDeleteThread(QtCore.QThread):
    def __init__(self, user, passwd, imap_server, use_ssl, index):
        QtCore.QThread.__init__(self)
        self.server = IMAPClient(imap_server, use_uid=True, ssl=use_ssl)
        self.user = user
        self.passwd = passwd
        self.index = index
        self.server.login(self.user, self.passwd)

    def run(self):
        self.server.select_folder('INBOX')
        # get all messages without the "DELETED" flag they are sorted from 
        # old->new, start with 1 and kicked out messages/elements DON'T MOVE UP!
        messages = self.server.search(['NOT DELETED'])

        # *index* is the QML listview index and sorted from new->old and beginns
        # with 0, so add +1 to compensate that in comparison to the *messages*.
        # Now subtract the index from the *messages* length to get number the
        # of the clicked message in the *messages* list.
        del_num = len(messages)-(self.index+1)

        # Last step - delete/move to trash the selected message from *messages*
        self.server.delete_messages(messages[del_num])

#        self.server.expunge()  #DELETES THE MESSAGE FOREVER SO COMMENTED OUT!
        print "MESSAGE "+str(del_num)+" DELETED"


class Signal(QtCore.QObject):
    ''' own signals '''
    receiving_done = QtCore.Signal()
