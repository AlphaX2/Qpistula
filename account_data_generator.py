#!/usr/bin/env python

import pickle

data = {'mail_adress': '',
        'inbox_username': '',
        'inbox_password': '',
        'inbox_server': '',
        'inbox_use_ssl': False,
        'smtp_server': '',
        'smtp_username': '',
        'smtp_password': '',
        'smtp_use_ssl': False
 }

with open("qpistula_login.cfg", "w") as cfg:
    pickle.dump(data, cfg)
