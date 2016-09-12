# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IEEESim.ui'
#
# Created: Sun Mar 13 15:53:28 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1440, 1440)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1440, 1440))
        MainWindow.setMaximumSize(QtCore.QSize(9600, 10000))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.robot = QtGui.QWidget(self.centralwidget)
        self.robot.setGeometry(QtCore.QRect(0, 1298, 100, 100))
        self.robot.setObjectName(_fromUtf8("robot"))
        MainWindow.setCentralWidget(self.centralwidget)
#        self.menubar = QtGui.QMenuBar(MainWindow)
#        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 42))
#        self.menubar.setObjectName(_fromUtf8("menubar"))
#        self.menuIEEE_Simulator = QtGui.QMenu(self.menubar)
#        self.menuIEEE_Simulator.setObjectName(_fromUtf8("menuIEEE_Simulator"))
#        self.menuTest = QtGui.QMenu(self.menubar)
#        self.menuTest.setObjectName(_fromUtf8("menuTest"))
#        MainWindow.setMenuBar(self.menubar)
#        self.menubar.addAction(self.menuIEEE_Simulator.menuAction())
#        self.menubar.addAction(self.menuTest.menuAction())

#        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuIEEE_Simulator.setTitle(_translate("MainWindow", "IEEE Simulator", None))
        self.menuTest.setTitle(_translate("MainWindow", "Test", None))

