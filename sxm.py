"""The main application"""
# -*- coding: latin-1 -*-
# TODO: make Makefiles platform-independent, then remove generated files from version control
# TODO: when the main window is closed, image windows should be closed as well

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def main():
    # import all the UI classes:
    sys.path.insert(0,'.')
    sys.path.insert(0,'..') # würg
    from gui.mainwindow import MainWindow
    import gui.sxmrc
    
    # create main QT application:
    app = QApplication(sys.argv)
    splashpixmap = QPixmap(":/images/images/splash.png")
    splash = QSplashScreen(splashpixmap) #,QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    a = Qt.AlignBottom
    splash.showMessage("PySPA starting...",a)
    app.processEvents()
    app.setStyle(QStyleFactory.create("Windows"))
    app.setQuitOnLastWindowClosed(True)
    
    # install translator
    trans = QTranslator(app)
    trans.load(':lang/sxmlang_en.qm')
    app.installTranslator(trans)
    app.processEvents()
    modulestring = "Loading"
    modulestring += " SciPy"
    splash.showMessage(modulestring,a)
    app.processEvents()
    import scipy
    modulestring += " PIL"
    splash.showMessage(modulestring,a)
    app.processEvents()
    import Image
    modulestring += " format plugins"
    splash.showMessage(modulestring,a)
    app.processEvents()
    from SXM import SM3
    import SXM.FileIO
    SXM.FileIO.init()
    modulestring += "."
    splash.showMessage(modulestring,a)
    app.processEvents()
    from SXM import Data
    
    # create and show main window
    win = MainWindow(app)
    win.show()
        
    splash.finish(win)
    
    # testing: start a dummy worker thread
##    worker = DummyThread()
##    worker.start()
    
    # run application event loop
    app.exec_()
    
##    if not worker.isFinished():
##        print "Asking worker thread to finish."
##        worker.stop()
##        print "Waiting for worker thread to finish..."
##        worker.wait()
##    else:
##        print "Worker thread has already finished."
    
    sys.exit()

class DummyThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.count = 0
        self.stopped = 0
        
    def run(self):
        while (self.count < 10) and not self.stopped:
            print "work... (%i)" % (self.count),
            self.count += 1
            self.sleep(1)
            
    def stop(self):
        self.stopped = 1

if __name__ == '__main__':
    main()


