import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
matplotlib.use("TkAgg")
def getValuesOverTimeRange(pvList):
        results = {}
        with open("test",'r') as f:
          for pv in pvList: 
              try:
                   response = f.read()
                   jsonData = json.loads(response)

                   element =jsonData.pop()
                   result = { "values":[]}
                   for datum in element[u'data']:
                        # result["times"].append(datum[u'secs'])
                        result["values"].append(datum[u'val'])

                   results[pv] = len(result["values"])


              except ValueError:

                   print("JSON error with {PVS}".format(PVS=pvList))

        f.close()
        # print(result)
        return results

if __name__ == "__main__":
    r = []
    rye = []
    testList = ["BEND:LTUH:220:BDES"]
    # print(archiver.getDataAtTime(testList, datetime.now()))
    r=getValuesOverTimeRange(testList)
    # rye = r ["BEND:LTUH:220:BDES"]["values"]
    # print(len(rye))
    print (r)
    #x = np.linspace(0, 2, 100)
    t=np.arange(0.0, 2.0, 0.01)
    s = 1+ np.sin(2*np.pi*t)
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='time',ylabel='voltage', title='About as simple as it gets')
    ax.grid()
    plt.show()

