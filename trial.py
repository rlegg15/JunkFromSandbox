#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 11:01:23 2021

@author: user
"""
import random
import datetime

startTime = 1621181251
endTime = startTime + 72000
results ={}

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
    
def getValuesOverTimeDummy(startTime, endTime,timeInterval=None):
    global results
    cavPv=[]
    pvList=makList()
    codeFlt = ["0:FB_SUM", "0:RFS:INTLK_FIRST", "0:RFREADYFORBEAM"]
    for pv in pvList:
        for i in range(3):
            cavPv.append(str(pv) + codeFlt[i])
    print(cavPv)
    for avP in cavPv:
        result={"values":[], "times":[]}
        ranGe = random.randint(1,9)
        for i in range(ranGe):
             result["values"].append(random.randint(0,10))
             eventTime=int((endTime-startTime)/ranGe)
             result["times"].append(i*eventTime+startTime)
        results[avP]=result

    
getValuesOverTimeDummy(startTime, endTime)

