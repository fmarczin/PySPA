import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_mainwindow import Ui_MainWindow
from about import AboutDialog
from imagewindow import ImageWindow
from timeit import Timer
import operator

class MainWindow(QMainWindow,Ui_MainWindow):
    """The main application window (the first thing appearing on your screen).
    
    The base class for this is maintained in Designer, and we use multiple
    inheritance.
    """
    def __init__(self, app):
        """initialize the mainwindow."""
        QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self) 

        self.Images = []
        
    def closeEvent(self, event):
        print 'Quitting...'
        for ch in self.Images:
            print type(ch)
            print 'closing %s' % ch.objectName()
            ch.close()
        event.accept()
        
        
    def setupUi(self, MainWindowBase):
        """setup the window.
        
        First, the method of the base class is called, and then all the
        functionality is installed (signal/slot connections mainly).
        """
        Ui_MainWindow.setupUi(self, MainWindowBase)
        self.widget = MainWindowBase
        QObject.connect(self.actionAbout,SIGNAL("triggered()"),self.openAbout)
        QObject.connect(self.actionFileOpen,SIGNAL("triggered()"),self.openFile)
        self.statusBar().showMessage(self.tr("Ready"))

    def openAbout(self):
        """Slot for opening the About box."""
        dlg = AboutDialog()
        dlg.show()
        dlg.exec_()

    def retranslateUi(self, MainWindow):
        Ui_MainWindow.retranslateUi(self, MainWindow)
        MainWindow.setWindowTitle(self.tr("MainWindow").arg("PySPA"))

    def openFile(self):
        """Slot for the openFile action."""
        from SXM import FileIO,Data
        fname = str(QFileDialog.getOpenFileName(self.widget,self.tr("Open File"), \
                ".",FileIO.getFilterString(types=(Data.Image,))))
        if len(fname) > 0:
            root, ext = os.path.splitext(fname)
            self.statusBar().showMessage(self.tr("Loading data: %1").arg(fname),2000)
            image = FileIO.fromFile(fname)
            image.load()
            imwin = ImageWindow(self,image)
            self.Images.append(imwin)
            self.updateImageList()
            imwin.windowModality = False
            imwin.show()
##            print ', '.join([str(i) for i in self.Images])
            
    def imageWindowClosed(self,image):
        self.Images.remove(image)
        self.updateImageList()
    
    def updateImageList(self):
        self.datalist.clear()
        for im in self.Images:
            self.datalist.addItem(str(im.SXMImage))
