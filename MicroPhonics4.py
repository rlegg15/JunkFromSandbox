from pydm import Display
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton)
from os import path, pardir
from qtpy.QtCore import Slot, QTimer
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
import glob
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
            return path.join(self.pathHere, fileName)
        self.xfDisp = Display(ui_filename=getPath("MicPlot.ui"))  
        XfelPlot = MplCanvas(self, width = 20, height =40, dpi=100)
         
        self.xfDisp.ui.Plot3.addWidget(XfelPlot)
        
        self.ui.StrtBut.clicked.connect(self.setGOVal)  # call function setGOVal when strtBut is pressed

        self.timer= QTimer()                            # start timer to track data acq     
        self.timer.timeout.connect(partial(self.showTime,XfelPlot))
                   

    def FFTPlot(self, ac,cavUno):   
        N = len(cavUno)
        T = 1.0/1000 
        x = np.linspace(0.0, N*T, N, endpoint=False)
        y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
        yf1 = fft(cavUno)
        xf = fftfreq(N, T)[:N//2]
        ac.axes.plot(xf, 2.0/N * np.abs(yf1[0:N//2]))

        
    def showTime(self,ac):
        global count
        self.ui.AcqProg.setText("Data Acquisition started. "+str(count)+" sec left.")	# decrementing the counter
        count -= 1
        if count<0:
            self.timer.stop()
            self.getDataBack(ac)
        return      

    def getUserVal(self):
        cavNumA=''
        cavNumB=''               
        cmNum = self.ui.spinBox_2.value()  # Get Cryomodule number from spinBox_2
        if cmNum==1:
            liNac="L0B" 
        elif cmNum > 1 and cmNum < 4:
            liNac = "L1B" 
        elif cmNum > 3 and cmNum < 16:
            liNac = "L2B"
        else:
            liNac = "L3B"
     
        if cmNum<10:                
            cmNumSt='0'+str(cmNum)
        else:
            cmNumSt=str(cmNum)           
                                                                 
        if self.ui.Cav1.isChecked():
            cavNumA=cavNumA+'1 '
        if self.ui.Cav2.isChecked():
            cavNumA=cavNumA+'2 '
        if self.ui.Cav3.isChecked():
            cavNumA=cavNumA+'3 '
        if self.ui.Cav4.isChecked():
            cavNumA=cavNumA+'4 '
        if self.ui.Cav5.isChecked():
            cavNumB=cavNumB+'5 '
        if self.ui.Cav6.isChecked():
            cavNumB=cavNumB+'6 ' 
        if self.ui.Cav7.isChecked():
            cavNumB=cavNumB+'7 ' 
        if self.ui.Cav8.isChecked():
            cavNumB=cavNumB+'8 ' 
        return liNac, cmNumSt, cavNumA, cavNumB


    def setGOVal(self):

        global count

        liNac, cmNumSt, cavNumA, cavNumB = self.getUserVal()
        print(cavNumA, cavNumB)        
        if cavNumA!='' or cavNumB!='':

            timMeas = self.ui.spinBox.value()  # Get time for measurement from spinBox            
            count=timMeas
# =============================================================================
# This is where the dir creation code needs to go and I need to change the shell
# script lines below to return the files to the correct directories.            
# =============================================================================
            if cavNumA != '':
                prStr = "python res_data_acq.py -D ~/data -a ca://ACCL:"+liNac+":"+str(cmNumSt)+"00:RESA: -wsp 2 -acav "+cavNumA+"-ch DAC DF -c "+str(int(timMeas//8)+(timMeas % 8 > 0))
                print(prStr)
            if cavNumB != '':
                prStr = "python res_data_acq.py -D ~/data -a ca://ACCL:"+liNac+":"+str(cmNumSt)+"00:RESB: -wsp 2 -acav "+cavNumB+"-ch DAC DF -c "+str(int(timMeas//8)+(timMeas % 8 > 0))
                print(prStr)
            
            self.timer.start(1000)   

        else:
            self.ui.AcqProg.setText("No Cavity selected. try again")
        return
    
    def getDataBack(self,ac):
        cavDat1=[]
        cavDat2=[]
        cavDat3=[]
        cavDat4=[]
        cavDat5=[]
        cavDat6=[]
        cavDat7=[]
        cavDat8=[]
        cavNumA=''
        cavNumB=''          
 
        liNac, cmNumSt, cavNumA, cavNumB = self.getUserVal()    
# =============================================================================
# This is where I need to add the code to go find the correct files to be read back in
# and I still need to parse the files to  read the data from the cavities selected
# =============================================================================
# #             pathDir="/PHYSICS_TOP/rf_lcls2/microphonics/"+"ACCL_"+liNac+"_"+str(cmNumSt)+str(cavNumA[0])+'0'
# #             print(pathDir)
# # #            dFDat = glob.glob(pathDir+'/res_cav'+str(cavNumA[0])+'*')
# #             dFDat = glob.glob('*')
#        dFDat = FFt_math.readCavDat(glob.glob(pathDir+'/res_cav'+str(cavNumA)+'*'))
# #             print(dFDat)
        dFDat = FFt_math.readCavDat("1234_20210617_1227")
        cavDat1,cavDat2,cavDat3,cavDat4 = FFt_math.parseCavDat(dFDat)
        dFDat = FFt_math.readCavDat("5678_20210617_1227")
        cavDat5,cavDat6,cavDat7,cavDat8 = FFt_math.parseCavDat(dFDat)
        
        
#     #            cavsAll = self.ui.Cavs58.isChecked() and self.ui.Cavs14.isChecked()
        indexPlot = self.ui.comboBox.currentIndex()        

        if indexPlot ==1:
                leGend=[]
                ac.axes.cla()
                if '1' in cavNumA:
                    ac.axes.hist(cavDat1, bins=140,  histtype='step', log='True', edgecolor='b')
                    leGend.append('Cav1')
                if '2' in cavNumA:
                    ac.axes.hist(cavDat2, bins=140,  histtype='step', log='True', edgecolor='r')
                    leGend.append('Cav2')
                if '3' in cavNumA:
                    ac.axes.hist(cavDat3, bins=140,  histtype='step', log='True', edgecolor='g')
                    leGend.append('Cav3')
                if '4' in cavNumA:
                    ac.axes.hist(cavDat4, bins=140,  histtype='step', log='True', edgecolor='c')
                    leGend.append('Cav4')
                if '5' in cavNumB:
                    ac.axes.hist(cavDat5, bins=140,  histtype='step', log='True', edgecolor='m')
                    leGend.append('Cav5')
                if '6' in cavNumB:
                    ac.axes.hist(cavDat6, bins=140,  histtype='step', log='True', edgecolor='y')
                    leGend.append('Cav6')
                if '7' in cavNumB:
                    ac.axes.hist(cavDat7, bins=140,  histtype='step', log='True', edgecolor='k')
                    leGend.append('Cav7')
                if '8' in cavNumB:
                    ac.axes.hist(cavDat8, bins=140,  histtype='step', log='True', edgecolor='w')                    
                    leGend.append('Cav8')
                ac.axes.set_xlim(-20, 20)
                ac.axes.set_ylim(bottom=1)
                ac.axes.set_xlabel('Detune in Hz')
                ac.axes.set_ylabel('Cnts')
                ac.axes.grid(True)
                ac.axes.legend(leGend)
                ac.draw_idle()  
               
        if indexPlot == 2:
                leGend=[]
                ac.axes.cla()
                if '1' in cavNumA:
                    self.FFTPlot(ac,cavDat1)
                    leGend.append('Cav1')
                if '2' in cavNumA:
                    self.FFTPlot(ac,cavDat2)
                    leGend.append('Cav2')
                if '3' in cavNumA:
                    self.FFTPlot(ac,cavDat3)
                    leGend.append('Cav3')
                if '4' in cavNumA:
                    self.FFTPlot(ac,cavDat4)
                    leGend.append('Cav4')
                if '5' in cavNumB:
                    self.FFTPlot(ac,cavDat5)
                    leGend.append('Cav5')
                if '6' in cavNumB:
                    self.FFTPlot(ac,cavDat6)
                    leGend.append('Cav6')
                if '7' in cavNumB:
                    self.FFTPlot(ac,cavDat7)
                    leGend.append('Cav7')
                if '8' in cavNumB:
                    self.FFTPlot(ac,cavDat8)                  
                    leGend.append('Cav8')
                ac.axes.set_xlim(0, 150)
                ac.axes.set_xlabel('Freq, Hz')
                ac.axes.set_ylabel('Rel Amplitude')
                ac.axes.grid(True)
                ac.axes.legend(leGend)
                ac.draw_idle()  
                     
        self.showDisplay(self.xfDisp)   
       
        if indexPlot==0:
            self.xfDisp.close()
            self.ui.AcqProg.setText("Microphonics data saved to file")              
        return
   
    def showDisplay(self, display):
        # type: (QWidget) -> None
        display.show()
        # brings the display to the front
        display.raise_()
        # gives the display focus
        display.activateWindow()
