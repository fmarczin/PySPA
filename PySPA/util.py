from decimal import Decimal
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def fmt(num,decimals=2):
    """Formats a number into a string via the Decimal module.
    
    num can be an int, float, Decimal or string.
    decimals can be used to set the precision.
    """
    if not isinstance(num,Decimal):
        if isinstance(num,float):
            num = Decimal(str(num))
        else:
            num = Decimal(num)
    exp = Decimal((0, (0,) * decimals, -decimals))
    return str(num.quantize(exp))

def SPFixedFixed():
    sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(False)
    return sizePolicy

def SPFixed():
    return SPFixedFixed()

def SPPrefPref():
    sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
##    sizePolicy.setHorizontalStretch(1)
##    sizePolicy.setVerticalStretch(1)
    sizePolicy.setHeightForWidth(False)
    return sizePolicy

def SPPref():
    return SPPrefPref()

def SPFixedPref():
    sizePolicy = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(False)
    return sizePolicy

