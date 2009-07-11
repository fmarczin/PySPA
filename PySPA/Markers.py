from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PointMarker:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def draw(self,p):
        """Draw a representation of the marker on the QPainter p"""
        pen = QPen()
        pen.setColor(QColor(255,0,0))
        pen.setStyle(Qt.SolidLine)
        p.setPen(pen)
        p.drawLine(self.x,self.y-5,self.x,self.y+5)
        p.drawLine(self.x-5,self.y,self.x+5,self.y)
