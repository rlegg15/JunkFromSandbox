from pydm import Display
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton)
from os import path, pardir
from qtpy.QtCore import Slot
#from pydm.widgets.template_repeater import PyDMTemplateRepeater
from typing import List, Dict
from functools import partial, reduce
from datetime import datetime, timedelta
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from random import randint, random
import datetime

b=[]
c=[]
RfStt=false
RfFlt=true
Vals=[]
Val2=[]
StD =[]
StD2=[]
MeanRec =[]
MeanRec2=[]
StDevRec=[]
StDevRec2=[]

# Build some dummy data arrays
for i in range(1,18):
   b.append(i)
   Vals.append(randint(0,40))
   StD.append(randint(0,10))
   MeanRec.append(random())
   StDevRec.append(random()/2)
for i in range(20,36):
   c.append(i)
   Val2.append(randint(0,40))
   StD2.append(randint(0,10))
   MeanRec2.append(random())
   StDevRec2.append(random()/2)

def printToTerminal(message):
    print(message)

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

        sc.axes.cla()
        sc.axes.bar(b, Vals, yerr=StD)
        sc.axes.set_ylabel('Faults')
        sc.axes.set_xlabel('L0B   L1B  HS                            L2B                                      ')
        sc2.axes.cla()
        sc2.axes.bar(c, Val2,yerr=StD2)
        sc2.axes.set_ylabel('Faults')
        sc2.axes.set_xlabel('L3B')
        self.ui.Plot1.addWidget(sc)
        self.ui.Plot2.addWidget(sc2)

        def rfFault():
            self.ui.label_7.setText("Blue Bars are RF Faults. Black lines are StDev of Cavity Faults")
            RfFl=True
            RfSt=False
            sc.axes.cla()
            sc.axes.bar(b, Vals, yerr=StD)
            sc.axes.set_ylabel('Faults')
            sc.axes.set_xlabel('L0B   L1B HS                            L2B                                      ')
            sc2.axes.cla()
            sc2.axes.bar(c, Val2,yerr=StD2)
            sc2.axes.set_ylabel('Faults')
            sc2.axes.set_xlabel('L3B')
            sc.draw_idle()
            sc2.draw_idle()
            return RfFl, RfSt

        def rfStat():
            self.ui.label_7.setText("Blue Bars are Mean Cav Rec Time. Black lines are StDev between cavities")
            #self.ui.Plot1.removeWidget(sc)
            #self.ui.Plot2.removeWidget(sc2) 
            sc.axes.cla()
            sc.axes.bar(b, MeanRec, yerr=StDevRec)
            sc.axes.set_ylabel('AveRecTime')
            sc.axes.set_xlabel('L0B   L1B HS                            L2B                                      ')
            print("Stats")
            sc2.axes.cla()
            sc2.axes.bar(c, MeanRec2,yerr=StDevRec2)
            sc2.axes.set_ylabel('AveRecTime')
            sc2.axes.set_xlabel('L3B')
            sc.draw_idle()
            sc2.draw_idle()

        RfFlt, RfStt= self.ui.FullModule.clicked.connect(rfFault)
        print(RfStt,RfFlt)
        self.ui.SingleCavity.clicked.connect(rfStat) 


   def showDisplay(self, display):
            # type: (QWidget) -> None
        display.show()
            # brings the display to the front
        display.raise_()
        # gives the display focus
        display.activateWindow()
