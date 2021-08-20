import numpy as np
import matplotlib.pyplot as plt
import statistics

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
#transpose =numpy_array.T
#flipped=transpose.tolist()


for testPV in PVList:
   Cavity.append(testPV)           # strip out the linac and cavity number from PV for plot
for i in range(len(numpy_array)):
   qnch.append(numpy_array[i][0])
 
plt.figure(figsize=(9,4))
plt.bar(Cavity,qnch, label='Sum')
plt.legend()
plt.xlabel('cavity')
plt.ylabel('# of faults')
plt.title("Faults per Cavity from ")
plt.grid()

plt.show()
