# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

class SimpleViewer(QMainWindow):
    def __init__(self,parent,image):
        """initialize the mainwindow."""
        QMainWindow.__init__(self,parent)

        self.SXMimage = image

        self.setupUi() 

    def setupUi(self):
        self.setObjectName("ImageWindow")
        self.resize(QtCore.QSize(QtCore.QRect(0,0,406,300).size()).expandedTo(self.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(self)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.imagedummy = QtGui.QLabel(self.imageframe)
        self.imagedummy.setMinimumSize(QtCore.QSize(150,150))
        self.imagedummy.setObjectName("imagedummy")
        self.hboxlayout.addWidget(self.imagedummy)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("SimpleViewer", "WindowTitle", None, QtGui.QApplication.UnicodeUTF8))
