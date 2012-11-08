#-*- coding: utf-8 -*-

import os
import sys
import pickle
import ConfigParser


from PySide import QtCore
from imapclient import IMAPClient

from MailWrapper import MailWrapper
from MailListModel import MailListModel

class MailAccount(QtCore.QObject):
    ''' holds account data and manage mail actions'''
    def __init__(self):
        QtCore.QObject.__init__(self)

        self.mails_model = None
        self.mail_check = None
        self.mail_search = None
        self.account_name = 'Mein Account'

        self.signal = Signal()
        self.settings = ConfigParser.ConfigParser()

        if os.path.exists(os.path.expanduser('~/.config/qpistula.cfg')):
            print "config existiert"
            self.read_conf()
        else:
            print "config existiert nicht, lege plain config file an"
            # should be replaced by popup settings-dialog
            self.default_conf()
            self.read_conf()

    def save_conf(self):
        with open(os.path.expanduser('~/.config/qpistula.cfg'), 'wb') as configfile:
            self.settings.write(configfile)

    def read_conf(self):
        self.settings.readfp(open(os.path.expanduser('~/.config/qpistula.cfg'), 'rwb'))
        self.inbox_server_type = self.settings.get(self.account_name,'inbox_server_type')
        self.mail_adress = self.settings.get(self.account_name, 'mail_adress')
        self.inbox_username = self.settings.get(self.account_name, 'inbox_username')
        self.inbox_password = self.settings.get(self.account_name, 'inbox_password')
        self.inbox_server = self.settings.get(self.account_name, 'inbox_server')
        self.inbox_use_ssl = self.settings.getboolean(self.account_name, 'inbox_use_ssl')
        self.smtp_server = self.settings.get(self.account_name, 'smtp_server')
        self.smtp_username = self.settings.get(self.account_name, 'smtp_username')
        self.smtp_password = self.settings.get(self.account_name, 'smtp_password', '')
        self.smtp_use_ssl = self.settings.get(self.account_name, 'smtp_use_ssl', 'False')
        self.update_interval = self.settings.getint(self.account_name, 'update_interval')

    # to generate plain config-file, should be deleted when settings dialog works
    def default_conf(self):
        self.settings.add_section(self.account_name)
        self.settings.set(self.account_name, 'inbox_server_type', 'None')
        self.settings.set(self.account_name, 'mail_adress', '')
        self.settings.set(self.account_name, 'inbox_username', '')
        self.settings.set(self.account_name, 'inbox_password', '')
        self.settings.set(self.account_name, 'inbox_server', '')
        self.settings.set(self.account_name, 'inbox_use_ssl', 'False')
        self.settings.set(self.account_name, 'smtp_server', '')
        self.settings.set(self.account_name, 'smtp_username', '')
        self.settings.set(self.account_name, 'smtp_password', '')
        self.settings.set(self.account_name, 'smtp_use_ssl', 'False')
        self.settings.set(self.account_name, 'update_interval','10')
        self.save_conf()

    def save_server_settings(self, server_type='', mail_adress='', user='', passwd='', server='', ssl='', smtp_username='', smtp_password= '', smtp_server= '', smtp_use_ssl = False):
        self.settings.set(self.account_name, 'inbox_server_type', server_type)
        self.settings.set(self.account_name, 'mail_adress', mail_adress)
        self.settings.set(self.account_name, 'inbox_username', user)
        self.settings.set(self.account_name, 'inbox_password', passwd)
        self.settings.set(self.account_name, 'inbox_server', server)
        self.settings.set(self.account_name, 'inbox_use_ssl', ssl)
        self.settings.set(self.account_name, 'smtp_server', smtp_server)
        self.settings.set(self.account_name, 'smtp_username', smtp_username)
        self.settings.set(self.account_name, 'smtp_password', smtp_password)
        self.settings.set(self.account_name, 'smtp_use_ssl', smtp_use_ssl)
        self.save_conf()

    def get_conf(self):
        server_type = self.inbox_server_type
        adress = self.mail_adress
        in_user = self.inbox_username
        in_pass = self.inbox_password
        in_server = self.inbox_server
        in_ssl = self.inbox_use_ssl
        out_server = self.smtp_server
        out_user = self.smtp_username
        out_pass = self.smtp_password
        out_ssl  = self.smtp_use_ssl

        conf_list = [server_type, adress, in_user, in_pass, in_server, in_ssl, out_user, out_pass, out_server, out_ssl]
        return conf_list

    def receive_mails(self, folder='INBOX'):
        '''
        Call this function to start the MailCheckThread receiving latest mails.
        And connect the receivingFinished signal to update your UI!
        '''
        self.mail_check = MailCheckDeleteThread(self.inbox_username, self.inbox_password,
                                                self.inbox_server, self.inbox_use_ssl)
        # create from server response a Qt/QML friendly model
        self.mail_check.finished.connect(self._create_mail_model)
        self.mails = self.mail_check.start()

    # When MailCheckThread finished this function creates a Qt/QML model
    def _create_mail_model(self):
        response = self.mail_check.response
        mails = [MailWrapper(id,response[id]['RFC822']) for id in reversed(response.keys())]
        self.mails_model = MailListModel(mails)
        self.signal.receiving_done.emit()

    def send_mail(self, destination, subject, content):
        # the accounts mail adress
        sender=self.mail_adress
        destination = destination.split(",") # get multiple mails adresses

        # typical values for text_subtype are plain, html, xml
        text_subtype = 'html' #'plain'

        if self.smtp_use_ssl:
            # this invokes the secure SMTP protocol (port 465, uses SSL)
            from smtplib import SMTP_SSL as SMTP
        else:
            # use this for standard SMTP protocol (port 25, no encryption)
            from smtplib import SMTP
        from email.MIMEText import MIMEText

        try:
            msg = MIMEText(content.encode('utf-8'), text_subtype, 'UTF-8')
            msg['Subject']= subject
            msg['From']   = sender
            msg['To'] = ','.join(destination)

            conn = SMTP(self.smtp_server)
            conn.set_debuglevel(False)
            conn.login(self.smtp_username, self.smtp_password)
            try:
                conn.sendmail(sender, destination, msg.as_string())
            finally:
                conn.close()
        except Exception, exc:
            sys.exit( "mail failed; %s" % str(exc) ) # give a error message

    def get_mails_model(self):
        return self.mails_model

    def delete_mails(self, uid):
        self.mail_delete = MailCheckDeleteThread(self.inbox_username, self.inbox_password,
                                                 self.inbox_server, self.inbox_use_ssl,
                                                 uid=uid)
        self.mail_delete.finished.connect(self.receive_mails)
        self.mail_delete.start()

class MailCheckDeleteThread(QtCore.QThread):
    def __init__(self, user, passwd, imap_server, use_ssl, uid=None, folder='INBOX'):
        QtCore.QThread.__init__(self)
        self.server = IMAPClient(imap_server, use_uid=True, ssl=use_ssl)
        self.user = user
        self.passwd = passwd
        self.server.login(self.user, self.passwd)

        self.response = {}
        self.uid = uid
        self.folder = folder

    def run(self):
        self.server.select_folder(self.folder)
        if not self.uid: # NO UID = NO MAIL TO DELETE
            print "refreshing"
            # just show not deleted messages in the INBOX!
            messages = self.server.search(['NOT DELETED'])
            self.response = self.server.fetch(messages, ['RFC822'])
        if self.uid:
            print "deleting"
            self.server.select_folder('INBOX')
            self.server.delete_messages(self.uid)


class Signal(QtCore.QObject):
    ''' own signals '''
    receiving_done = QtCore.Signal()
