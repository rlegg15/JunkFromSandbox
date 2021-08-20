# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 17:08:16 2021

@author: bob
"""
import scipy.fft
#from scipy.fft import fft, fftfreq

import numpy as np
cavDat1 = [] 
cavDat2 = [] 
cavDat3 = []
cavDat4 = []
read_data=[]

with open('1234_20210617_1227') as f:
    for lin in range(28):
        header_Data = f.readline()
    read_data = f.readlines()
   
f.close()
# Number of sample points

for red in read_data:
    cavDat1.append(float(red[10:18]))
    cavDat2.append(float(red[30:38]))
    cavDat3.append(float(red[50:58]))
    cavDat4.append(float(red[70:78]))
#print(cavDat3)

N = len(cavDat1)

# sample spacing

T = 1.0/1000 

x = np.linspace(0.0, N*T, N, endpoint=False)
#print(len(data))

#y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)

#yf1 = fft(cavDat1)
#yf2 = fft(cavDat2)
#yf3 = fft(cavDat3)
#yf4 = fft(cavDat4)
#xf = fftfreq(N, T)[:N//2]

import matplotlib.pyplot as plt

#plt.plot(xf, 2.0/N * np.abs(yf1[0:N//2]))
#plt.plot(xf, 2.0/N * np.abs(yf2[0:N//2]))
#plt.plot(xf, 2.0/N * np.abs(yf3[0:N//2]))
#plt.plot(xf, 2.0/N * np.abs(yf4[0:N//2]))
#weights = np.ones_like(cavDat1)/float(len(cavDat1))
#plt.hist(cavDat1, weights=weights)

plt.hist(cavDat1, bins=140,  histtype='step', log='True', edgecolor='b')
plt.hist(cavDat2, bins=140,  histtype='step', log='True', edgecolor='r')
plt.hist(cavDat3, bins=140,  histtype='step', log='True', edgecolor='g')
plt.hist(cavDat4, bins=140,  histtype='step', log='True', edgecolor='c')
plt.xlim(-50, 50)
plt.xlabel('Detune in Hz')
plt.ylabel('Cnts')
#plt.plot(x,cavDat)
plt.grid()
plt.legend(['Cav1', 'Cav2','Cav3','Cav4'])
plt.show()