import argparse
import datetime
import json
import requests
import numpy
import random

ARCHIVER_URL_FORMATTER = "http://{MACHINE}-archapp.slac.stanford.edu/retrieval/data/{{SUFFIX}}"
SINGLE_RESULT_SUFFIX = "getDataAtTime?at={TIME}-07:00&includeProxies=true"
RANGE_RESULT_SUFFIX = "getData.json"
TIMEOUT = 3
class Archiver(object):


    def __init__(self, machine):
        # type: (str) -> None
        self.url_formatter = ARCHIVER_URL_FORMATTER.format(MACHINE=machine)

    def getValuesOverTimeRange(self, pvList, startTime, endTime, timeInterval=None):
        # type: (List[str], datetime, datetime, int) -> Dict[str, Dict[str, List[Union[datetime, str]]]]
        url = self.url_formatter.format(SUFFIX=RANGE_RESULT_SUFFIX)
        results = {}
        for pv in pvList:
                   response = requests.get(url=url, timeout=TIMEOUT,
                                           params={"pv": pv,
                                                   "from": startTime.isoformat() + "-07:00",
                                                   "to": endTime.isoformat() + "-07:00"})
                   results = {}

                   try:
                       jsonData = json.loads(response.text)
                       element = jsonData.pop()
                       result = {"times": [], "values": []}
                       for datum in element[u'data']:
                           result["times"].append(datum[u'secs'])
                           result["values"].append(datum[u'val'])

                       results[pv] = result

                   except ValueError:
                       print("JSON error with {PVS}".format(PVS=pvList))


        return results
#******************************************************

#******************************************************
def makList():
    #################
    # this function generates a PV list for cavities
    # in SC linac
    #################

    pvList = []
    for lin in range(4):     #  for the 4 linac sections
        if lin == 0:         #  start with L0B
            for j in range(1, 9):
                pvList.append("ACCL:L" + str(lin) + "B:01" + str(j))
        if lin == 1:         # move to L1B and do two 1.3GHz CM
            for n in range(2, 4):
                for j in range(1, 9):
                    pvList.append("ACCL:L" + str(lin) + "B:" + "0" + str(n) + str(j))
                             # then do the H1 and H2 3.9 GHz CM
            for n in range(1, 3):
                for j in range(1, 9):
                    pvList.append("ACCL:L" + str(lin) + "B:" + "H" + str(n) + str(j))
                             # move on to the 12 CMs in L2B
        if lin == 2:
            for n in range(4, 16):
                if n < 10:
                    for j in range(1, 9):
                        pvList.append("ACCL:L" + str(lin) + "B:" + "0" + str(n) + str(j))
                             # remember to adjust CM number in PV if greater than '10'
                else:
                    for j in range(1, 9):
                        pvList.append("ACCL:L" + str(lin) + "B:" + str(n) + str(j))
                             # Finally, do the 20 CMs in L3B
        if lin == 3:
            for n in range(16, 36):
                for j in range(1, 9):
                    pvList.append("ACCL:L" + str(lin) + "B:" + str(n) + str(j))
    return pvList;
#******************************************************

#******************************************************
def cmFlts(stTim, endTim):
    cc="01"
    b=[]
    c=[]
    dd=[]
    total=[]
    totalLo = []
    totalHi=[]
    stDev=[]
    stDLo=[]
    stDHi=[]
    results={}
    results2 ={}

    pvL = makList()

##################
#  The commented out block calls the archiver for the interlock and clipping faults
#############
    #cavPv = []
    #reFbSults=[]
    #reIntlkSults = []
    #codeFlt = ["0:FB_SUM", "0:RFS:INTLK_FIRST", "0:RFREADYFORBEAM"]
    #for pv in pvL:
    #    for i in range(2):
    #        cavPv.append(str(pv) + codeFlt[i])
    #    result = archiver.getValuesOverTimeRange(cavPv[0], stTim, endTim)
    #    result2 = archiver.getValuesOverTimeRange(cavPv[1], stTim, endTim)
#############
# ******  Remove the lines below to use archiver rather than dummy data
    for pv in pvL:
        result={"values":[]}
        result2 = {"values": []}
        for i in range(random.randint(1,5)):
             result["values"].append(random.randint(0,10))
             result2["values"].append(random.randint(0, 10))
        results[pv]=result["values"] + result2["values"]
        results2[pv]=len(result["values"])  + len(result2["values"])
#************************

    aaaa = results2.keys()

    for app in aaaa:
        bb=str(app)
        if bb[9:11] == cc:
            dd.append(results2[app])
        else:
            xx=numpy.array(dd)
            total.append(numpy.sum(xx))
            stDev.append(numpy.std(xx))
            cc = bb[9:11]
            dd=[]
            dd.append(results2[app])
    xx = numpy.array(dd)
    total.append(numpy.sum(xx))
    stDev.append(numpy.std(xx))
    for i in range(17):
        totalLo.append(total[i])
        stDLo.append(stDev[i])
        b.append(i+1)
    for i in range(17,37):
        totalHi.append(total[i])
        stDHi.append(stDev[i])
        c.append(i+1)
    return b,c,totalLo, totalHi, stDLo, stDHi;
#****************************************************

#****************************************************
def sortStats(CavFlts, CavRdy):
    i=0
    n=0
    FltTime=[]
    dd=[]
    while i <= (len(CavFlts) - 1):
       Flt = CavFlts[i]
       Rdy =CavRdy[n]

       if (int(Rdy) >= int(Flt)) and ((i + 1) <= len(CavFlts)) and ((n + 1) <= len(CavRdy)):
           FltTime.append(int(Rdy) - int(Flt))
           while (int(Flt) <= int(Rdy)) and ((i + 1) <= len(CavFlts)):
              try:
                i += 1
                if (i + 1) <= len(CavFlts):
                   Flt = CavFlts[i]
                continue
              except IndexError:
                #print("incremented i too far")
                break

       elif (int(Flt) >= int(Rdy)) and ((n + 1) < len(CavRdy)):
           try:
              while (Flt >= Rdy):
                n += 1
                Rdy = CavRdy[n]
                continue
           except IndexError:
              #print("incremented n too far")
              break
       else:
           break
    if cavFaults==[]:
       FltTime=0

    return FltTime;
#***************************************************

#***************************************************
def CmStats(stTim, endTim):
    cc="00"
    b=[]
    c=[]
    dd=[]
    cavTot =[]
    CMtot=[]
    total=[]
    totalLo = []
    totalHi=[]
    average=[]
    stDev=[]
    stDLo=[]
    stDHi=[]
    results={}
    results2 ={}

    pvL = makList()
##################
#  The commented out block calls the archiver for the interlock and clipping faults
#############
    #cavPv = []
    #reFbSults=[]
    #reIntlkSults = []
    #codeFlt = ["0:FB_SUM", "0:RFS:INTLK_FIRST", "0:RFREADYFORBEAM"]
    #for pv in pvL:
    #    for i in range(2):
    #        cavPv.append(str(pv) + codeFlt[i])
    #    result = archiver.getValuesOverTimeRange(cavPv[1], stTim, endTim)
    #    result2 = archiver.getValuesOverTimeRange(cavPv[2], stTim, endTim)
#############

    for pv in pvL:
        result={"times":[]}
        result2 = {"times": []}
        for i in range(random.randint(1,7)):
             result["times"].append(random.randint(9950,10000))
             result2["times"].append(random.randint(9950, 10000))
        results[pv]=sorted(result["times"])  #this is the time of the faults
        results2[pv]=sorted(result2["times"])  # this is the time that rf shows fully recovered

    aaaa = results.keys()

    for cav in aaaa:
        i = 0
        n = 0
        CavFltDat = (results[cav])  # get the flt times for a single cavity
        CavRdyDat = (results2[cav])  #get the recover times for a single cavity
        dd=[]
        dd=sortStats(CavFltDat,CavRdyDat)
        xx = numpy.array(dd)
        cavTot.append(numpy.sum(dd)/60)
    #print(cavTot)
    #print(len(cavTot))
    for n in range(0,37):
        CMtot=[]
        for i in range(0,8):
            CMtot.append(cavTot[i+n*8])
        total.append(numpy.sum(CMtot))
        average.append(numpy.mean(CMtot))
        stDev.append(numpy.std(CMtot))

    for i in range(17):
        totalLo.append(average[i])
        stDLo.append(stDev[i])
        b.append(i+1)
    for i in range(17,37):
        totalHi.append(average[i])
        stDHi.append(stDev[i])
        c.append(i+1)
    return b,c,totalLo, totalHi, stDLo, stDHi;
#***************************************************

#***************************************************
def makCavPv(spinOut):
    pv2 = []
    pvL = ""
    cav = []
    # print(spinOut)
    if spinOut == "H1" or spinOut == "H2":
        pvL = "ACCL:L1B:" + spinOut
    else:
        if int(spinOut) == 1:
            pvL = "ACCL:L0B:" + str(spinOut)
        if 1 < int(spinOut) < 4:
            pvL = "ACCL:L1B:" + str(spinOut)
        if 3 < int(spinOut) < 10:
            pvL = "ACCL:L2B:" + str(spinOut)
        if 9 < int(spinOut) < 16:
            pvL = "ACCL:L2B:" + str(spinOut)
        if 15 < int(spinOut) < 36:
            pvL = "ACCL:L3B:" + str(spinOut)
    for i in range(1, 9):
        alpha = pvL + str(i) + "0"
        # print(alpha)
        pv2.append(alpha)
        cav.append(str(spinOut) + str(i))
    if str(spinOut) == "Not":
        pv2 = "NaN"
    return pv2, cav;
#***********************************************
#
#
def cavDatCnt(caVs, sT, fiN):
    results={}
    if caVs != "NaN":
        # cavPv = []
        # reFbSults=[]
        # reIntlkSults = []
        # codeFlt = ["0:FB_SUM", "0:RFS:INTLK_FIRST", "0:RFREADYFORBEAM"]
        # for pv in pvLow:
        #    for i in range(2):
        #        cavPv.append(str(pv) + codeFlt[i])
        #    result = archiver.getValuesOverTimeRange(cavPv[0], sT, fiN)
        #    result2 = archiver.getValuesOverTimeRange(cavPv[1], sT, fiN)
        for pv in caVs:
            result = {"values": []}
            result2 = {"values": []}
            for i in range(random.randint(1, 5)):
                result["values"].append(random.randint(0, 10))
                result2["values"].append(random.randint(0, 10))

            #
            #  bozo and clwn are variables to count the number for each type of fault in the dataset
            #  fault code '1' is PLL lock, '2' is ioc watchdog, '4' is the Interlock Fault summary, '8' is Comm fault
            #  '16' is an SSA fault and '32 is a cavity quench
            #
            bozo = {"PLLlock": [], "iocDog": [], "IntlkFlt": [], "CommFlt": [], "SSAFlt": [],
                    "Quench": [], "Clips": []}
            clwn = []
            clwn = result["values"]  # read 'values' into clwn list
            bozo["PLLlock"] = clwn.count(1)
            bozo["iocDog"] = clwn.count(2)
            bozo["IntlkFlt"] = clwn.count(4)
            bozo["CommFlt"] = clwn.count(8)
            bozo["SSAFlt"] = clwn.count(16)
            bozo["Quench"] = clwn.count(32)
            bozo["Clips"] = len(result2["values"])
            results[pv] = bozo
    else:
        results = []
    return results;
#
#***********************************************
def cavFaults(cmUpper, cmLower, Start, End):
    if cmUpper != "Not":
        pvCav, cavU = makCavPv(cmUpper)
        resP = cavDatCnt(pvCav,Start, End)
    else:
        cavU = []
        resP=[]
    if  cmLower != "Not":
        pvCav, cavL =makCavPv(cmLower)
        resP2 = cavDatCnt(pvCav, Start, End)
    else:
        cavL=[]
        resP2=[]
    return cavU, cavL, resP, resP2;
#******************************************************
#
def cavStatCnt(Cav, Start, End):
     cc="00"
     dd=[]
     xx=[]
     cavAve=[]
     cavStD=[]
     results={}
     results2 ={}
     ##################
    #  The commented out block calls the archiver for the interlock and clipping faults
    #############
    #cavPv = []
    #reFbSults=[]
    #reIntlkSults = []
    #codeFlt = ["0:FB_SUM", "0:RFS:INTLK_FIRST", "0:RFREADYFORBEAM"]
    #for ca in Cav:
    #    for i in range(2):
    #        cavPv.append(str(Cav) + codeFlt[i])
    #    result = archiver.getValuesOverTimeRange(cavPv[0], Start, End)
    #    result2 = archiver.getValuesOverTimeRange(cavPv[1], Start, End)
    #############

     for ca in Cav:
        result={"times":[]}
        result2 = {"times": []}
        for i in range(random.randint(1,15)):
             result["times"].append(random.randint(0,10000))
             result2["times"].append(random.randint(0, 10000))
        results[ca]=sorted(result["times"])  #this is the time of the faults
        results2[ca]=sorted(result2["times"])  # this is the time that rf shows fully recovered

     aaaa = results.keys()

     for cav in aaaa:
        i = 0
        n = 0
        CavFltDat = (results[cav])  # get the flt times for a single cavity
        CavRdyDat = (results2[cav])  #get the recover times for a single cavity
        dd=[]
        dd=sortStats(CavFltDat,CavRdyDat)
        xx = numpy.array(dd)
        if len(xx) > 1:
            cavAve.append(numpy.mean(xx)/60)
            cavStD.append(numpy.std(xx)/60)
        elif len(xx) == 1:
            cavAve.append(dd[0]/60)
            cavStD.append(0)
        else:
            cavAve.append(0)
            cavStD.append(0)
        #print("cavAve=",cavAve,"cavStD=",cavStD)
     return cavAve, cavStD;
#**********************************************
#
#
#***********************************************
def cavStats(cmUpper,cmLower, Start, End):
     if cmUpper != "Not":
        pvCav, cavU = makCavPv(cmUpper)
        resPave, resPstd = cavStatCnt(pvCav,Start,End)
     else:
        cavU =[]
        resPave =[]
        resPstd =[]
     if cmLower != "Not":
        pvCav2, cavU2 = makCavPv(cmLower)
        resPave2, resPstd2 = cavStatCnt(pvCav2,Start,End)
     else:
         cavU2=[]
         resPave2 = []
         resPstd2 = []
     return cavU, cavU2, resPave, resPstd, resPave2, resPstd2;


if __name__ == "__main__":
    archiver = Archiver("lcls")
    #e,f,DisLow,DisHi, DisLoStd, DisHiStd = CmStats(datetime.time,datetime.time)
    #print(len(DisLow),len(DisHi))
    e, f, r1,r2,r3,r4  = cavStats("Not","27",datetime.time,datetime.time)
    print("e=",e,"\r\n", r1,"\r\n",r2)

