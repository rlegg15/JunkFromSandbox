import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
matplotlib.use("TkAgg")
def getValuesOverTimeRange(pvList):
        results = {}
        with open("cavData",'r') as f:
          for pv in pvList: 
              try:
                   response = f.read()
                   jsonData = json.loads(response)

                   element =jsonData.pop()
                   result = { "values":[]}
                   for datum in element[u'data']:
                        # result["times"].append(datum[u'secs'])
                        result["values"].append(datum[u'val'])

                   results[pv] = result


              except ValueError:

                   print("JSON error with {PVS}".format(PVS=pvList))

        f.close()
        # print(result)
        return results

if __name__ == "__main__":
    r = []
    rye = []
    testList = ["ACCL:L0B:0120:RFS:INTLK_FIRST"]
    # print(archiver.getDataAtTime(testList, datetime.now()))
    r=getValuesOverTimeRange(testList)
    # print(r)
    #rye = len(r["ACCL:L0B:0120:RFS:INTLK_FIRST"]["values"])
    for testPV in testList:
        rye = len(r[testPV]["values"])
        
    plt.figure(figsize=(9,3))
    plt.bar(testList,rye)
    #plt.plot(x, x, label='linear')  # Plot some data on the (implicit) axes.
    #plt.plot(x, x**2, label='quadratic')  # etc.
    #plt.plot(x, x**3, label='cubic')
    plt.xlabel('cavity')
    plt.ylabel('# of faults')
    plt.title("Faults per Cavity")
    #x = np.linspace(0, 2, 100)
    #t=np.arange(0.0, 2.0, 0.01)
    #s = 1+ np.sin(2*np.pi*t)
    #fig, ax = plt.subplots()
    #ax.plot(t, s)
    #ax.set(xlabel='time',ylabel='voltage', title='About as simple as it gets')
    #ax.grid()
    plt.show()

