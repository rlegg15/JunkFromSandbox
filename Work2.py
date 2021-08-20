from pydm import Display
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox)
from os import path, pardir
from qtpy.QtCore import Slot
#from pydm.widgets.template_repeater import PyDMTemplateRepeater
from typing import List, Dict
from functools import partial, reduce
from datetime import datetime, timedelta
from requests import post
from csv import reader
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from random import randint

sys.path.insert(0, '..')
b=[]
c=[]
Vals=[]
Val2=[]
StD =[]
StD2=[]
frameNum=0

for i in range(17):
   b.append(i)
   Vals.append(randint(0,40))
   StD.append(randint(0,10))
for i in range(21):
   c.append(i)
   Val2.append(randint(0,40))
   StD2.append(randint(0,10))

def printToTerminal(message):
    print(message)

def GetDates(a,b):
    print(a, b)

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout="true")
        self.axes = fig.add_subplot(111)
        fig.align_labels()        
        super(MplCanvas, self).__init__(fig)

class Training(Display):
    def __init__(self, parent=None, args=None, ui_filename="Training.ui"):
        super(Training,self).__init__(parent=parent,args=args,ui_filename=ui_filename)
        
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc2 = MplCanvas(self, width=5, height=4, dpi=100)
        # TODO get rid of meaningless test data
        sc.axes.bar(b, Vals, yerr=StD)
        sc.axes.set_ylabel('Faults')
        sc.axes.set_xlabel('L0B   L1B                            L2B                                      ')
        
        sc2.axes.bar(c, Val2,yerr=StD2)
        sc2.axes.set_ylabel('Faults')
        sc2.axes.set_xlabel('L3B')

        self.ui.Plot1.addWidget(sc)
        self.ui.Plot2.addWidget(sc2)

        val=self.ui.StartTime.dateTime() 
        val2 = self.ui.EndTime.dateTime()
        self.ui.GO.clicked.connect(partial(GetDates,val,val2))
        
             
    

def showDisplay(self, display):
            # type: (QWidget) -> None
   display.show()

            # brings the display to the front
   display.raise_()

        # gives the display focus
   display.activateWindow()
