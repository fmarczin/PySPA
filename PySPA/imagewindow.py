# -*- coding: latin-1 -*-
from Markers import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from decimal import Decimal
from util import * 
import cStringIO

# TODO: use the decimal module for number displays (maybe for calculations too?)
# TODO: make the image window more aware of non-height (eg. dIdU) images

class ImageWindow(QMainWindow):
    """An image window.
    
    G{classtree}
    """
    
    (SMPoint) = range(1)
    
    def __init__(self,parent,image):
        """initialize the mainwindow."""
        QMainWindow.__init__(self,parent)

        self.main = parent
        self.SXMImage = image

        # Set up the Scene:
        self.scene = QGraphicsScene(0, 0, 1, 1, self)
        
        # Set up the user interface:
        self.setupUi() 
        self.dataChanged()

        # install processing menuitems:
        self.menuProcBackground.addAction(self.tr("Row-wise z-Offset"),self.bgRowwiseZOffset)
        self.menuProcBackground.addAction(self.tr("Column-wise z-Offset"),self.bgColwiseZOffset)
        actionPlaneSubtract = QAction(self)
        actionPlaneSubtract.setText(self.tr("Plane subtract"))
        actionPlaneSubtract.setIcon(QIcon(":/images/images/plane.png"))
        QObject.connect(actionPlaneSubtract,SIGNAL("triggered()"),self.bgPlaneSubtract)
        self.menuProcBackground.addAction(actionPlaneSubtract)
        self.toolbar.addAction(actionPlaneSubtract)
        
        
    def show(self):
        QMainWindow.show(self)
        self.adjustSize()
        
    def setupUi(self):
        """setup the window.
        """
        self.setObjectName("ImageWindow")
        self.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
        
        self.centralwidget = QWidget(self)
        #self.centralwidget.setSizePolicy(QSizePolicy.Preferred)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QHBoxLayout(self.centralwidget)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.hboxlayout.setObjectName("hboxlayout")
        
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.vboxlayout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        self.imagelabel = QLabel(self.centralwidget)
        self.imagelabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.imagelabel.setTextFormat(Qt.RichText)
        self.imagelabel.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.imagelabel.setMargin(0)
        self.imagelabel.setIndent(0)
        self.imagelabel.setObjectName("imagelabel")
        
        self.theimage = ImageWidget(self.scene, self.centralwidget)
        self.theimage.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.theimage.setObjectName("Image")
        
        self.vboxlayout.addWidget(self.imagelabel)
        self.vboxlayout.addWidget(self.theimage)
        
        self.rangeWidget = RangeWidget()
        
        QObject.connect(self.rangeWidget,SIGNAL("changed()"),self.limitsChanged)
        
        self.vboxlayout1 = QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.vboxlayout1.setObjectName("vboxlayout1")

        zoom = ZoomSettingsWidget(self)

        self.vboxlayout1.addWidget(self.rangeWidget)
        self.vboxlayout1.addWidget(zoom)
        self.vboxlayout1.addStretch(1)

        self.hboxlayout.addLayout(self.vboxlayout)
        self.hboxlayout.addLayout(self.vboxlayout1)
        
        self.setCentralWidget(self.centralwidget)
        
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        self.menuProcess = QMenu(self.menubar)
        self.menuProcess.setObjectName("menuProcess")
        
        self.menuProcBackground = QMenu(self.menuProcess)
        self.menuProcBackground.setObjectName("menuProcBackground")
        
        self.menuView = QMenu(self.menubar)
        
        self.setMenuBar(self.menubar)
        self.toolbar = QToolBar(self)
        self.toolbar.setWindowTitle(self.tr("Image processing"))
        
        self.addToolBar(self.toolbar)
        
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        self.actionClose = QAction(self)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionClose)
        self.menuProcess.addAction(self.menuProcBackground.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProcess.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        
        # "Save Image"-Action 
        self.actionSaveImage = QAction(self)
        self.actionSaveImage.setObjectName("actionSaveImage")
        self.menuFile.addAction(self.actionSaveImage)
        QObject.connect(self.actionSaveImage,SIGNAL("triggered()"),self.saveImage)

        # "View/Adjust window size"-Action 
        self.actionAdjWinSize = QAction(self)
        self.menuView.addAction(self.actionAdjWinSize)
        QObject.connect(self.actionAdjWinSize,SIGNAL("triggered()"),self.adjustSize)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self):
        self.setWindowTitle(self.tr("%1 (%2)").arg(self.SXMImage.Name).arg(self.SXMImage.ImageType))
        self.imagelabel.setText(self.tr('<b>%1 %2 <font color="#0000ff">%3</font> <font color="#ff0000">%4</font></b>').arg(self.SXMImage.Name).arg("(%s)" % (self.SXMImage.ImageType)).arg("U: %s V" % (fmt(self.SXMImage.UBias))).arg("I: %s nA" % (fmt(self.SXMImage.ISet,3)))) 
        self.menuFile.setTitle(self.tr("File"))
        self.menuProcess.setTitle(self.tr("Process"))
        self.menuProcBackground.setTitle(self.tr("Background"))
        self.menuView.setTitle(self.tr("View"))
        self.actionClose.setText(self.tr("Close"))
        self.actionSaveImage.setText(self.tr("Save Image"))
        self.actionAdjWinSize.setText(self.tr("Fit window to image"))

    def dataChanged(self):
        self.scene.setSceneRect(0, 0, self.SXMImage.XRes, self.SXMImage.YRes)
        lower = Decimal(str(self.SXMImage.dataMin))*Decimal(str(self.SXMImage.ZScale))
        lower = float(lower.normalize())
        upper = Decimal(str(self.SXMImage.dataMax))*Decimal(str(self.SXMImage.ZScale))
        upper = float(upper.normalize())
        self.rangeWidget.setDataRange(lower,upper)
        self.limitsChanged()
    
    def limitsChanged(self):
        self.dispmin,self.dispmax = self.rangeWidget.getRange()
        self.updateDisplay()
        
    def updateDisplay(self):
        PILstring = cStringIO.StringIO()
        self.SXMImage.toImage(PILstring,"bmp",cmin=self.dispmin/float(self.SXMImage.ZScale),cmax=self.dispmax/float(self.SXMImage.ZScale))
        PILstring.seek(0)
        self.qimage = QImage(self.SXMImage.XRes,self.SXMImage.YRes,QImage.Format_RGB32)
        self.qimage.loadFromData(PILstring.read())
        del PILstring
        self.theimage.setqimage(self.qimage)
        self.updateGeometry()

    def bgRowwiseZOffset(self):
        self.SXMImage.bgRowwiseZOffset()
        self.dataChanged()
         
    def bgColwiseZOffset(self):
        self.SXMImage.bgColwiseZOffset()
        self.dataChanged()    
        
    def bgPlaneSubtract(self):
        self.SXMImage.bgPlaneSubtract()
        self.dataChanged()    
        
    def saveImage(self):
        fname = QFileDialog.getSaveFileName(self,self.tr("Enter filename"),".","Images (*.png *.xpm *.jpg)")
        self.SXMImage.saveImage(str(fname))
        
    def adjustWinSize(self):
        pass
        
    def closeEvent(self, event):
        self.main.imageWindowClosed(self)
    
class ImageWidget(QGraphicsView):
    def __init__(self,scene, parent=None):
        QGraphicsView.__init__(self,scene, parent)
        self.setRenderHints(QPainter.SmoothPixmapTransform)
        self.pixmapitem = QGraphicsPixmapItem(None, scene)
        self.pixmapitem.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self.pixmapitem.setTransformationMode(Qt.SmoothTransformation)
        self.maxSize = QSize()

    def setqimage(self,qimage):
        self.qimage = qimage
        self.pixmapitem.setPixmap(QPixmap.fromImage(self.qimage))
        self.sizeChanged()

    def sizeChanged(self):
        self.maxSize = QSize(self.matrix().m11()*self.qimage.width() + 2*self.frameWidth(),  self.matrix().m22()*self.qimage.height() + 2*self.frameWidth())
        self.setMaximumSize(self.maxSize)
        self.updateGeometry()
    
    def sizeHint(self):
        return self.maxSize

    def zoomIn(self):
        self.scale(1.2, 1.2)
        self.sizeChanged()
    
    def zoomOut(self):
        self.scale(0.7, 0.7)
        self.sizeChanged()
    
    def toggleSmooth(self, state):
        if state == Qt.Checked:
            self.pixmapitem.setTransformationMode(Qt.SmoothTransformation)
        else:
            self.pixmapitem.setTransformationMode(Qt.FastTransformation)
            
class RangeWidget(QGroupBox):
    def __init__(self,parent=None):
        self.dispmin = Decimal('0.0')
        self.dispmax = Decimal('0.0')
        
        QGroupBox.__init__(self,parent)
        
        self.setTitle(self.tr("Display range"))

        self.setSizePolicy(SPFixed())
        self.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        # main layout
        self.vboxlayout = QVBoxLayout(self)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)

        # grid layout
        self.gridlayout = QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)

        # the labels saying "Min" and "Max"
        self.minlabel = QLabel(self)
        self.minlabel.setText(self.tr("Min"))
        self.minlabel.setSizePolicy(SPFixedPref())
        self.minlabel.setObjectName("minlabel")
        self.gridlayout.addWidget(self.minlabel,2,0,1,1)
        self.maxlabel = QLabel(self)
        self.maxlabel.setText(self.tr("Max"))
        self.maxlabel.setSizePolicy(SPFixedPref())
        self.maxlabel.setObjectName("maxlabel")
        self.gridlayout.addWidget(self.maxlabel,1,0,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        # the two spinboxes
        self.displimitmin = QDoubleSpinBox(self)
        self.displimitmin.setSizePolicy(SPFixed())
        self.displimitmin.setMinimumSize(QSize(40,0))
        self.displimitmin.setMaximum(100000.0)
        self.displimitmin.setMinimum(-100000.0)
        self.displimitmin.setObjectName("displimitmin")
        self.gridlayout.addWidget(self.displimitmin,2,1,1,1)
        self.minlabel.setBuddy(self.displimitmin)

        self.displimitmax = QDoubleSpinBox(self)
        self.displimitmax.setSizePolicy(SPFixed())
        self.displimitmax.setMinimumSize(QSize(40,0))
        self.displimitmax.setMaximum(100000.0)
        self.displimitmax.setMinimum(-100000.0)
        self.displimitmax.setObjectName("displimitmax")
        self.gridlayout.addWidget(self.displimitmax,1,1,1,1)
        self.maxlabel.setBuddy(self.displimitmax)

        # the two checkboxes for locking the spinbox value to the
        # max/min of the data
        self.limitslockdatamin = QCheckBox(self)
        self.limitslockdatamin.setObjectName("limitslockdatamin")
        self.limitslockdatamin.setChecked(True)
        self.gridlayout.addWidget(self.limitslockdatamin,2,2,1,1)

        self.limitslockdatamax = QCheckBox(self)
        self.limitslockdatamax.setObjectName("limitslockdatamax")
        self.limitslockdatamax.setChecked(True)
        self.gridlayout.addWidget(self.limitslockdatamax,1,2,1,1)

        # and the label above them
        self.locklabel = QLabel(self)
        self.locklabel.setText(self.tr("lock to data"))
        self.locklabel.setObjectName("locklabel")
        self.gridlayout.addWidget(self.locklabel,0,2,1,1)

        QObject.connect(self.limitslockdatamin,SIGNAL("toggled(bool)"),self.limitsChanged)
        QObject.connect(self.limitslockdatamax,SIGNAL("toggled(bool)"),self.limitsChanged)
        QObject.connect(self.displimitmin,SIGNAL("valueChanged(double)"),self.limitsChanged)
        QObject.connect(self.displimitmax,SIGNAL("valueChanged(double)"),self.limitsChanged)

    def setDataRange(self,min,max):
        self.datamin = min
        self.datamax = max
        if self.limitslockdatamin.isChecked():
            self.dispmin = self.datamin
            self.displimitmin.setValue(self.datamin)
        if self.limitslockdatamax.isChecked():
            self.dispmax = self.datamax
            self.displimitmax.setValue(self.datamax)
        
    def getRange(self):
        return self.dispmin, self.dispmax
    
    def limitsChanged(self):
        if self.limitslockdatamin.isChecked():
            self.dispmin = self.datamin
            self.displimitmin.setValue(self.datamin)
        else:
            self.dispmin = self.displimitmin.value()
        if self.limitslockdatamax.isChecked():
            self.dispmax = self.datamax
            self.displimitmax.setValue(self.datamax)
        else:
            self.dispmax = self.displimitmax.value()

        self.emit(SIGNAL('changed()'))
        
class NiceSpinBox(QDoubleSpinBox):
    def __init__(self,parent):
        QDoubleSpinBox(self,parent)
        
class ZoomSettingsWidget(QGroupBox):
    def __init__(self,parent):
        QGroupBox.__init__(self,parent)
        self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.setObjectName("ZoomSettingsGroupBox")
        
        zoomin = QPushButton(self)
        zoomin.setText(self.tr("+"))
        QObject.connect(zoomin, SIGNAL('clicked()'), parent.theimage.zoomIn)
        zoomout = QPushButton(self)
        zoomout.setText(self.tr("-"))
        QObject.connect(zoomout, SIGNAL('clicked()'), parent.theimage.zoomOut)
        
        smoothtoggle = QCheckBox()
        smoothtoggle.setText(self.tr("Interpolate"))
        smoothtoggle.setCheckState(Qt.Unchecked)
        QObject.connect(smoothtoggle, SIGNAL('stateChanged(int)'), parent.theimage.toggleSmooth)

        layout = QGridLayout(self)
        layout.addWidget(zoomin, 0, 0, Qt.AlignLeft|Qt.AlignTop)
        layout.addWidget(zoomout,  1, 0, Qt.AlignLeft|Qt.AlignTop)
        layout.addWidget(smoothtoggle,  2, 0, Qt.AlignLeft|Qt.AlignTop)
        self.setLayout(layout)
        self.retranslateUi()
        
    def retranslateUi(self):
        self.setTitle(self.tr("Zoom"))
