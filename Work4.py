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
from requests import post
from csv import reader
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from random import randint, random
import datetime

sys.path.insert(0, '..')
b=[]
c=[]
Vals=[]
Val2=[]
StD =[]
StD2=[]
MeanRec =[]
MeanRec2=[]
StDevRec=[]
StDevRec2=[]
frameNum=0 

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

        self.pathHere = path.dirname(sys.modules[self.__module__].__file__)
        def getPath(fileName):
            return path.join(self.pathHere, fileName)
  
        self.selectWindow = Display(ui_filename=getPath("CMSelector.ui"))
        self.ui.CMSelection.clicked.connect(partial(self.showDisplay,
                                                       self.selectWindow))
        #self.selectWindow.ui.Sel_Instructions.setText("No CM Selected. Try again")
        #if self.ui.CMSelection.isChecked():
            #print("got this far")
            #self.showDisplay(self.selectWindow)
            #self.selectWindow.ui.Sel_Instructions.setText("One Cryomodule may be selected for each of the Upper and Lower plots")
            #self.ui.CMSelection.toggle()


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
        #self.ui.Plot1.removeWidget(sc)

        val=self.ui.StartTime.dateTime() 
        val2 = self.ui.EndTime.dateTime()
        self.ui.GO.clicked.connect(partial(self.setVal))
   
        def RfFault():
            self.ui.label_7.setText("Blue Bars are RF Faults. Black lines are StDev of Cavity Faults")
            #self.ui.Plot1.removeWidget(sc)
            #self.ui.Plot2.removeWidget(sc2)            
            sc.axes.cla()
            sc.axes.bar(b, Vals, yerr=StD)
            sc.axes.set_ylabel('Faults')
            sc.axes.set_xlabel('L0B   L1B HS                            L2B                                      ')
            print("Faults")
            sc2.axes.cla()
            sc2.axes.bar(c, Val2,yerr=StD2)
            sc2.axes.set_ylabel('Faults')
            sc2.axes.set_xlabel('L3B')
            self.ui.Plot1.addWidget(sc)
            self.ui.Plot2.addWidget(sc2)

        def RfStat():
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
            self.ui.Plot1.addWidget(sc)
            self.ui.Plot2.addWidget(sc2)

        if self.ui.FullModule.isChecked():
            RfFltDisp = 1
            RfStatDisp = 0
            print(RfFltDisp, RfStatDisp)        
        if self.ui.SingleCavity.isChecked():
            RfFltDisp = 0
            RfStatDisp = 1 
            print(RfFltDisp, RfStatDisp)
        #self.ui.FullModule.clicked.connect(RfFault)        
        #self.ui.SingleCavity.clicked.connect(RfStat) 

   def clear(self):
        item = self.ui.Plot1.itemAt(2)
        print(item)
        if item != None :
            widget = item.widget()
            print(widget)
            if widget != None:
                self.ui.Plot1.removeWidget(widget)
                widget.deleteLater()  

   def updateSelectedText(self):
        if not self.selectedDisplayCMs:
            self.ui.Changes.setStyleSheet("color: red;")
            self.ui.Changes.setText("No Cryomodules Selected")
            #self.calibrationFrame.setEnabled(False)
            #self.rfFrame.setEnabled(False)

        else:
            self.ui.Changes.setStyleSheet("color: green;")
            self.ui.Changes.setText(str(sorted(self.selectedDisplayCMs))
                                             .replace("'", "").replace("[", "")
                                             .replace("]", ""))
            #self.calibrationFrame.setEnabled(True)

   def setVal(self):
        #CmNumber_1=self.selectWindow.getval
        val=self.ui.StartTime.dateTime() 
        val2 = self.ui.EndTime.dateTime()
        StTimeForArchiver=val.toPyDateTime().strftime('%m/%d/%Y %H:%M:%S')
        EndTimeForArchiver=val2.toPyDateTime().strftime('%m/%d/%Y %H:%M:%S') 
        cmNumUpper = self.selectWindow.ui.Plot_1.value()
        cmNumLower = self.selectWindow.ui.Plot_2.value()
        HSUpper = self.selectWindow.ui.HS_Upper.value()
        HSLower = self.selectWindow.ui.HS_Lower.value()
        if (cmNumUpper != 0 and HSUpper!=0) or (cmNumLower !=0 and HSLower!=0):
           self.selectWindow.ui.Sel_Instructions.setText("Only one CM per plot.  Try again")
        elif ((cmNumUpper == 0 and HSUpper==0) and (cmNumLower ==0 and HSLower ==0)):
           self.ui.Changes.setStyleSheet("color: red;")
           self.ui.Changes.setText("No Cryomodules Selected.")
           self.selectWindow.ui.Sel_Instructions.setText("No CM Selected. Try again")           
        else:
           self.selectWindow.close()
           self.selectWindow.ui.Sel_Instructions.setText("One Cryomodule may be selected for each of the Upper and Lower plots")
           self.ui.Changes.setStyleSheet("color: green;")
           if cmNumUpper != 0:
              OutTextUpper = cmNumUpper
           elif HSUpper!=0:
              OutTextUpper = "HS"+str(HSUpper)
           else:
              OutTextUpper = "Not"

           if cmNumLower != 0:
              OutTextLower = cmNumLower
           elif HSLower!=0:
              OutTextLower = "HS"+str(HSLower)
           else:
              OutTextLower = "Not"
           StrOut=("CM "+str(OutTextUpper)+" selected. CM "+str(OutTextLower)+" selected.")
           self.ui.Changes.setText(StrOut)
           #print(StrOut,StTimeForArchiver,EndTimeForArchiver) 
   

   def showDisplay(self, display):
            # type: (QWidget) -> None
        display.show()
            # brings the display to the front
        display.raise_()
        # gives the display focus
        display.activateWindow()
