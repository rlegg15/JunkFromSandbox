import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import statistics
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object, 
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        ListA = [[ 10003, 10004,10005,10010,  10020, 10033,  10042],
	   [ 10022, 10026,  10030,  10037, 10042],
	   [ 10008,  10014, 10026, 10033, 10045],
	   [ 10005,  10018, 10029, 10042,  10047],
	   [10020, 10033, 10039, 10044],
	   [10006, 10015, 10034, 10039, 10047],
	   [10004, 10009, 10013, 10019, 10027, 10033,10038, 10044],
	   [10015, 10032, 10044]]
        ListB = [[ 10007, 10016,  10023, 10037,  10048],
	   [ 10025, 10028,  10034,  10041, 10046],
	   [ 10010,  10017, 10029, 10039, 10048],
	   [ 10007,  10021, 10032, 10046,  10050],
	   [10023, 10036, 10042, 10050],
	   [10009, 10019, 10037, 10042, 10049],
	   [10007, 10012, 10016, 10022, 10030, 10036,10042, 10048],
	   [10018, 10035, 10047]]
        PVList = [110, 120,130,140,150,160,170,180]

        CavFltDat=[]
        CavRdyDat = []
        Flt=[]
        Rdy=[]
        lofl = []
        b=0
        Cavity = []
        qnch=[]

        for b in range (len(PVList)):
           i=0
           n=0
           CavFltDat=(ListA[b])
	   CavRdyDat=(ListB[b])
	   FltTime=[]
		
	   while i <= (len(CavFltDat)-1):
	      Rdy = CavRdyDat[n]
		 Flt = CavFltDat[(i)]	
		 if (int(Rdy) >= int(Flt)) and ((i+1) <= len(CavFltDat)) and ((n+1) <= len(CavRdyDat)):
		     FltTime.append( int(Rdy) - int(Flt))
				
                        while (int(Flt) <= int(Rdy)) and ((i+1) <= len(CavFltDat)):
			   try:
			      i+=1
			      if (i+1) <= len(CavFltDat):
			         Flt = CavFltDat[i]
				 continue
                           except IndexError:
			         print("Ooops, went too far with i")
				 break
				
			elif (int(Flt)>=int(Rdy)) and ((n+1) < len(CavRdyDat)):
					try:
						while(Flt>=Rdy):
							n+=1
							Rdy = CavRdyDat[n]
							continue
					except IndexError:
						print("ran off edge of map")
						break
			else:
				break

			
		if (i>0 and n>0):

			lofl.append([sum(FltTime),statistics.mean(FltTime),statistics.stdev(FltTime)])

	numpy_array = np.array(lofl)

	for testPV in PVList:
	   Cavity.append(testPV)           # strip out the linac and cavity number from PV for plot
	for i in range(len(numpy_array)):
	   qnch.append(numpy_array[i][0])
	 
	
	self.bar(Cavity,qnch, label='Sum')
	#self.legend()
	#plt.xlabel('cavity')
	#plt.ylabel('# of faults')
	#plt.title("Faults per Cavity from ")
	#plt.grid()

        self.setCentralWidget(sc)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
