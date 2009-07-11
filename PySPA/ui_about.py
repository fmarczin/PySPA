# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_about.ui'
#
# Created: Thu Jul 05 17:20:28 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(QtCore.QSize(QtCore.QRect(0,0,302,167).size()).expandedTo(AboutDialog.minimumSizeHint()))
        AboutDialog.setModal(True)

        self.layoutWidget = QtGui.QWidget(AboutDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(0,130,301,33))
        self.layoutWidget.setObjectName("layoutWidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(10,31,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.okButton = QtGui.QPushButton(self.layoutWidget)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)

        spacerItem1 = QtGui.QSpacerItem(10,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)

        self.label = QtGui.QLabel(AboutDialog)
        self.label.setGeometry(QtCore.QRect(10,10,281,111))
        self.label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label.setFrameShadow(QtGui.QFrame.Raised)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(1)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),AboutDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("AboutDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AboutDialog", "AboutText", None, QtGui.QApplication.UnicodeUTF8))

import main_rc
