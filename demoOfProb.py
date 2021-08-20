from pydm import Display
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton)
from os import path, pardir, makedirs
from qtpy.QtCore import Slot, QTimer
from functools import partial, reduce
from datetime import datetime, timedelta
import sys


class MicDisp(Display):

    def __init__(self, parent=None, args=None, ui_filename="FFT_test.ui"):
        super(MicDisp, self).__init__(parent=parent, args=args, ui_filename=ui_filename)
        self.pathHere = path.dirname(sys.modules[self.__module__].__file__)
#        print(self.pathHere)
        self.ui.StrtBut.clicked.connect(self.setGOVal)
  
        self.timer= QTimer() 
        self.timer.timeout.connect(self.showTime)

    def showTime(self):
        global count
        self.ui.AcqProg.setText("Data Acquisition started. "+str(count)+" sec left.")	# decrementing the counter
        count -= 1
        if count<0:
            self.timer.stop()
            self.getDataBack()
        return

    def setGOVal(self):
        global count
        timMeas = self.ui.spinBox.value()  # Get time for measurement from spinBox            
        count=timMeas
        print(count)
        self.timer.start(1000)
        
        return ("This is it")

    def getDataBack(self):
        print("count is ", count)
        print ("got beyond timer")
        # Now go get data and plot
        return
 