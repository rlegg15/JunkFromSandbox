import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import statistics
import json
matplotlib.use("TkAgg")
def getValuesOverTimeRange(pvList):

        with open("cavData3",'r') as f:
          results = {}
          response = []
          for pv in pvList: 
              try:
                   response = f.readline()
                   jsonData = json.loads(response)
                   
                   element =jsonData.pop()
                   result = { "values":[]}
                   for datum in element[u'data']:
                        # result["times"].append(datum[u'secs'])
                        result["values"].append(datum[u'val'])

                   #print(result)
                   results[pv] = len(result["values"])


              except ValueError:

                   print("JSON error with {PVS}".format(PVS=pvList))

        f.close()
        #print(result)
        return results

if __name__ == "__main__":
    r = []
    rye = []
    testList = []
    cm=[]
    cav=[0]
    CmFltMean = []
    CmNum = []
    CmFltStD=[]
    CmCavFlt= []
    fltLog=[]
    FltTot=[]

    for n in range(1,9):
         testList.append("ACCL:L0B:01"+str(n)+"0:RFS:INTLK_FIRST")

    #print(testList)

    r=getValuesOverTimeRange(testList)
    for j in range(15):
       cav = []
       for i in range(8):
          cav.append(0)
       CmCavFlt.append(cav)
    #print(CmCavFlt)
    #CmCavFlt[1][0] = 3
    #print(CmCavFlt)
    for test in testList:
       cm=int(test[9:11])
       cav=int(test[11:12])
       rye=r[test]
       #print("cm=",cm,"cav=",cav,"flt=",rye)
       CmCavFlt[(cm-1)][(cav-1)] = rye
       
    for i in range(15):
       CmFltMean.append(statistics.mean(CmCavFlt[i]))   
       CmFltStD.append(statistics.stdev(CmCavFlt[i]))
       CmNum.append(i+1)
       #print("CM=",i+1, "Mean Flts =", CmFltMean[i], "StD in cav flt # =",CmFltStD[i])
       
            
    plt.figure(figsize=(9,4))
    plt.bar(CmNum,CmFltMean, yerr=CmFltStD, label='Mean Flts and StdDev')
    #plt.bar(Cavity,PLL, bottom=qnch, label='PLL lock')
    #plt.bar(Cavity,ioc, bottom=plaid,label='IOC Watchdog')
    #plt.bar(Cavity,SSA, bottom=suede,label='SSA Flt')
    #plt.bar(Cavity,Intlk, bottom=twill, label='Intlk Flt Sum')
    #plt.bar(Cavity,com, bottom=gingham, label='Comm Fault')
    plt.legend()
    plt.xlabel('Cryomodule #')
    plt.ylabel('Mean # of faults')
    plt.title("Ave Faults and StdDev of Cavities in CM")
    plt.grid()
    plt.show()           

#    N = 5
 #  womenMeans = (25, 32, 34, 20, 25)
#    menStd = (2, 3, 4, 1, 2)
 #   womenStd = (3, 5, 2, 3, 3)
  #  ind = np.arange(N)    # the x locations for the groups
   # width = 0.35       # the width of the bars: can also be len(x) sequence

    #p1 = plt.bar(ind, menMeans, yerr=menStd)
    #p2 = plt.bar(ind, womenMeans, width,
     #        bottom=menMeans, yerr=womenStd)

   # plt.ylabel('Scores')
   # plt.title('Scores by group and gender')
   # plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
   # plt.yticks(np.arange(0, 81, 10))
   # plt.legend((p1[0], p2[0]), ('Men', 'Women'))

   # plt.show()

