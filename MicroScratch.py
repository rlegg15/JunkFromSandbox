from pydm import Display
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton)
from os import path, pardir
from qtpy.QtCore import (Slot, QTimer)
import time as t
# from pydm.widgets.template_repeater import PyDMTemplateRepeater
#from typing import List, Dict
from functools import partial, reduce
from datetime import datetime, timedelta
import sys
import numpy as np
from scipy.fftpack import fft, fftfreq
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from random import randint, random
import datetime
import FFt_math



class MplCanvas(FigureCanvasQTAgg):
# MPLCanvas is the class for the 'canvas' that plots are drawn on and then mapped to the ui
# They are Figure format described in matplotlib 2.2 documentation

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout="true")
        self.axes = fig.add_subplot(111)
        #fig.align_labels()  This was removed since only available in version 3 and later of matplotlib

        super(MplCanvas, self).__init__(fig)


class MicDisp(Display):

    def __init__(self, parent=None, args=None, ui_filename="FFT_test.ui"):
        super(MicDisp, self).__init__(parent=parent, args=args, ui_filename=ui_filename)
        self.pathHere = path.dirname(sys.modules[self.__module__].__file__)

        def getPath(fileName):
            return path.join(self.pathHere, fileName)  # This is supposed to find the path to the file named
                                                       # so that the files don't always have to be in the same dir
        UpperPlot = MplCanvas(self, width=5, height=4, dpi=100)  #This defines the plot sizes and attributes
        LowerPlot = MplCanvas(self, width=5, height=4, dpi=100)  # as matplotlib Figures
        XfelPlot = MplCanvas(self, width = 20, height =40, dpi=100)
         
        #self.selectWindow = Display(ui_filename=getPath("CMSelector.ui"))  # Set the 'selectWindow' to the cryomodule
        self.xfDisp = Display(ui_filename=getPath("MicPlot.ui"))   
        self.xfDisp.ui.Plot3.addWidget(XfelPlot)
        #self.ui.CMSelection.clicked.connect(self.CM_Sel)                   # When the CMSelection button is clicked,
        self.showDisplay(self.xfDisp)   
        self.ui.StrtBut.clicked.connect(self.cntDown(10))

#    def show_result(self):
#        spinVal = i
#        dispVal = self.ui.RfFltSel.currentText()
#        print(spinVal, dispVal)
        
    def cntDown(self, timToGo):
        self.ui.AcqProg.setText("Data Acquisition started. "+str(int(timToGo))+" sec left.")             
        #print(timMeas)     
        for i in range(timToGo):
            self.ui.AcqProg.setText("Data Acquisition started. "+str(int(timToGo)-i)+" sec left.")
            t.sleep(1)
            print(i)
        return()

    def FFTPlot(self, ac,cavUno,cavDos,cavTres,cavQuat):   
        N = len(cavUno)
        T = 1.0/1000 
        x = np.linspace(0.0, N*T, N, endpoint=False)
        y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
        yf1 = fft(cavUno)
        yf2 = fft(cavDos)
        yf3 = fft(cavTres)
        yf4 = fft(cavQuat)
        xf = fftfreq(N, T)[:N//2]
        ac.axes.plot(xf, 2.0/N * np.abs(yf1[0:N//2]))
        ac.axes.plot(xf, 2.0/N * np.abs(yf2[0:N//2]))
        ac.axes.plot(xf, 2.0/N * np.abs(yf3[0:N//2]))
        ac.axes.plot(xf, 2.0/N * np.abs(yf4[0:N//2]))
        weights = np.ones_like(cavUno)/float(len(cavUno))
        ac.axes.hist(cavUno, weights=weights)
        ac.axes.set_xlim(0, 150)
        ac.axes.set_xlabel('Freq, Hz')
        ac.axes.set_ylabel('Rel Amplitude')
        ac.axes.grid(True)
           

    def setGOVal(self,ac):
        cavDat1=[]
        cavDat2=[]
        cavDat3=[]
        cavDat4=[]
        cavDat5=[]
        cavDat6=[]
        cavDat7=[]
        cavDat8=[]
        
        cmNum = self.ui.spinBox_2.value()  # Get Cryomodule number from spinBox_2
        if cmNum==1:
            liNac="L0B"  
        elif cmNum > 1 and cmNum < 4:
            liNac = "L1B" 
        elif cmNum > 3 and cmNum < 16:
            liNac = "L2B"
        else:
            liNac = "L3B"
            
        timMeas = self.ui.spinBox.value()  # Get time for measurement from spinBox
        
        if (self.ui.Cavs14.isChecked() or self.ui.Cavs58.isChecked()) ==False:
            self.ui.AcqProg.setText("No cavities selected.  Please try again")                                                                  
        elif self.ui.Cavs14.isChecked():
            prStr = "python res_data_acq.py -D ~/data -a ca://ACCL:"+liNac+":"+str(cmNum)+"00:RESA: -wsp 2 -acav 1 2 3 4 -ch DAC DF -c "+str(int(timMeas//8)+(timMeas % 8 > 0))
            print(prStr)
        elif self.ui.Cavs58.isChecked():
            prStr = "python res_data_acq.py -D ~/data -a ca://ACCL:"+liNac+":"+str(cmNum)+"00:RESA: -wsp 2 -acav 5 6 7 8 -ch DAC DF -c "+str(int(timMeas//8)+(timMeas % 8 > 0))
            print(prStr) 
        indexPlot = self.ui.comboBox.currentIndex()
        
        self.cntDown(timMeas)

        if self.ui.Cavs14.isChecked() and indexPlot!=0:
            dFDat = FFt_math.readCavDat("1234_20210617_1227")
            cavDat1,cavDat2,cavDat3,cavDat4 = FFt_math.parseCavDat(dFDat)
        if self.ui.Cavs58.isChecked() and indexPlot!=0:
            dFDat = FFt_math.readCavDat("5678_20210617_1227")
            cavDat5,cavDat6,cavDat7,cavDat8 = FFt_math.parseCavDat(dFDat)
        cavsAll = self.ui.Cavs58.isChecked() and self.ui.Cavs14.isChecked()
#        print(indexPlot)
        if indexPlot > 0:
            if indexPlot ==1:
                if self.ui.Cavs14.isChecked() and (cavsAll==False):
                    ac.axes.cla()
                    ac.axes.hist(cavDat1, bins=140,  histtype='step', log='True', edgecolor='b')
                    ac.axes.hist(cavDat2, bins=140,  histtype='step', log='True', edgecolor='r')
                    ac.axes.hist(cavDat3, bins=140,  histtype='step', log='True', edgecolor='g')
                    ac.axes.hist(cavDat4, bins=140,  histtype='step', log='True', edgecolor='c')
                    ac.axes.set_xlim(-20, 20)
                    ac.axes.set_ylim(bottom=1)
                    ac.axes.set_xlabel('Detune in Hz')
                    ac.axes.set_ylabel('Cnts')
                    ac.axes.grid(True)
                    ac.axes.legend(['Cav1', 'Cav2','Cav3','Cav4'])
                    ac.draw_idle() 
                    
                elif self.ui.Cavs58.isChecked() and (cavsAll==False):
                    ac.axes.cla()
                    ac.axes.hist(cavDat5, bins=140,  histtype='step', log='True', edgecolor='b')
                    ac.axes.hist(cavDat6, bins=140,  histtype='step', log='True', edgecolor='r')
                    ac.axes.hist(cavDat7, bins=140,  histtype='step', log='True', edgecolor='g')
                    ac.axes.hist(cavDat8, bins=140,  histtype='step', log='True', edgecolor='c')
                    ac.axes.set_xlim(-20, 20)
                    ac.axes.set_ylim(bottom=1)
                    ac.axes.set_xlabel('Detune in Hz')
                    ac.axes.set_ylabel('Cnts')
                    ac.axes.grid(True)
                    ac.axes.legend(['Cav1', 'Cav2','Cav3','Cav4'])
                    ac.draw_idle()  
                    
                else:
                    ac.axes.cla()
                    ac.axes.hist(cavDat1, bins=140,  histtype='step', log='True', edgecolor='b')
                    ac.axes.hist(cavDat2, bins=140,  histtype='step', log='True', edgecolor='r')
                    ac.axes.hist(cavDat3, bins=140,  histtype='step', log='True', edgecolor='g')
                    ac.axes.hist(cavDat4, bins=140,  histtype='step', log='True', edgecolor='c')
                    ac.axes.hist(cavDat5, bins=140,  histtype='step', log='True', edgecolor='m')
                    ac.axes.hist(cavDat6, bins=140,  histtype='step', log='True', edgecolor='y')
                    ac.axes.hist(cavDat7, bins=140,  histtype='step', log='True', edgecolor='k')
                    ac.axes.hist(cavDat8, bins=140,  histtype='step', log='True', edgecolor='w')                    
                    ac.axes.set_xlim(-20, 20)
                    ac.axes.set_ylim(bottom=1)
                    ac.axes.set_xlabel('Detune in Hz')
                    ac.axes.set_ylabel('Cnts')
                    ac.axes.grid(True)
                    ac.axes.legend(['Cav1', 'Cav2','Cav3','Cav4','Cav5','Cav6','Cav7','Cav8'])
                    ac.draw_idle()  
                    
            if indexPlot == 2:
                if self.ui.Cavs14.isChecked() and (cavsAll==False):
                    ac.axes.cla()
                    self.FFTPlot(ac,cavDat1,cavDat2,cavDat3, cavDat4)
                    ac.axes.legend(['Cav1', 'Cav2','Cav3','Cav4'])
                    ac.draw_idle()  
                    
                elif self.ui.Cavs58.isChecked() and (cavsAll==False):
                    ac.axes.cla()
                    self.FFTPlot(ac,cavDat5,cavDat6,cavDat7, cavDat8) 
                    ac.axes.legend(['Cav5', 'Cav6','Cav7','Cav8'])
                    ac.draw_idle()   
                    
                else:
                    ac.axes.cla()
                    self.FFTPlot(ac,cavDat1,cavDat2,cavDat3, cavDat4)
                    self.FFTPlot(ac,cavDat5,cavDat6,cavDat7, cavDat8) 
                    ac.axes.legend(['Cav1', 'Cav2','Cav3','Cav4','Cav5','Cav6','Cav7','Cav8'])
                    ac.draw_idle()    
                    
         # "Sel_Instructions label" in the ui
        return()

       
    
    def showDisplay(self, display):
        # type: (QWidget) -> None
        display.show()
        # brings the display to the front
        display.raise_()
        # gives the display focus
        display.activateWindow()
