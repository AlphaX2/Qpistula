#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import imaplib
from PySide import QtGui, QtDeclarative, QtCore
import libqpistula

#QtOpenGL
reload(sys)
sys.setdefaultencoding('utf-8')

class Qpistula(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.view = QtDeclarative.QDeclarativeView()
        self.view.setSource('qml/main.qml')
        self.root = self.view.rootObject()
        self.context = self.view.rootContext()

#Starten der App
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    qpistula = Qpistula()
    qpistula.view.show()
    sys.exit(app.exec_())
