from PyQt4 import QtCore, QtGui
from ui_about import Ui_AboutDialog

class AboutDialog(QtGui.QDialog,Ui_AboutDialog):
   def __init__(self):
      QtGui.QDialog.__init__(self)
      self.setupUi(self)
   
   def retranslateUi(self, AboutDialogBase):
      AboutDialogBase.setWindowTitle(self.tr("Dialog").arg("PySPA"))
      self.okButton.setText(self.tr("OK"))
      self.label.setText(self.tr("AboutText").arg("PySPA").arg("v. 0.0.1"))
