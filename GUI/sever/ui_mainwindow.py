# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IEEESim.ui'
#
# Created: Tue Feb 16 20:00:27 2016
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
        MainWindow.resize(960, 960)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(960, 960))
        MainWindow.setMaximumSize(QtCore.QSize(9600, 10000))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 920, 50, 40))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 42))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuIEEE_Simulator = QtGui.QMenu(self.menubar)
        self.menuIEEE_Simulator.setObjectName(_fromUtf8("menuIEEE_Simulator"))
        self.menuTest = QtGui.QMenu(self.menubar)
        self.menuTest.setObjectName(_fromUtf8("menuTest"))
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuIEEE_Simulator.menuAction())
        self.menubar.addAction(self.menuTest.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "^", None))
        self.menuIEEE_Simulator.setTitle(_translate("MainWindow", "IEEE Simulator", None))
        self.menuTest.setTitle(_translate("MainWindow", "Test", None))

