# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:20:57 2020

@author: Vegard
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


    
def calculate_distance(data,i):
    # Get the three microphones
    #[Ts, data] = raspi_import("./stens.bin")

    # Seperate the three mics and remove DC
    mic1 = signal.detrend(data[:,0], type="constant") 
    mic2 = signal.detrend(data[:,1], type="constant")
    mic3 = signal.detrend(data[:,2], type="constant")

    length = len(mic1) # Get length of samples

    # Crosscorrelation
    xcorr21 = np.correlate(mic1, mic2, "full")
    xcorr31 = np.correlate(mic1, mic3, "full")
    xcorr32 = np.correlate(mic2, mic3, "full")
    
    if(i == 10):
        plt.plot(xcorr21)
        plt.plot(xcorr31)
        plt.plot(xcorr32)
        plt.show()

    # Get max lag
    maxlag21 = np.argmax(xcorr21) - length
    maxlag31 = np.argmax(xcorr31) - length
    maxlag32  = np.argmax(xcorr32) - length


    # Calculate angle
    # Lame calculations
    # theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))

    # Calculate angles cool way B-)

    xish = (-1/2*maxlag21 + 1/2*maxlag31 + maxlag32)
    b = xish < 0
    theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    while(theta > np.pi/2):
        theta -= np.pi
    return -theta
    
    
    
## Generate some shiiit
N = 100
c = 343
d = 0.07
Fs = 31250
thetas = np.linspace(-90*np.pi/180, 90*np.pi/180, num=N)
thetaestimates = np.zeros(N)
length = 50
M = 3

ns=np.linspace(0,N-1,num=N)


n = np.linspace(0,(length-1)/3, num=length)
sig = 0
for i in range(M):
    sig += np.sin(i*n)
    

maxlag = int(np.ceil(d/np.sqrt(3)/c*Fs))


for i in range(N):
    data = np.zeros((length-2*maxlag,3))
    lag1 = int(maxlag*np.cos(thetas[i]-np.pi/2))
    lag2 = int(maxlag*np.cos(thetas[i]+30*np.pi/180))
    lag3 = int(maxlag*np.cos(thetas[i]+150*np.pi/180))
    
    data[:,0] = sig[maxlag+lag1:len(sig)-(maxlag-lag1)]
    data[:,1] = sig[maxlag+lag2:len(sig)-(maxlag-lag2)]
    data[:,2] = sig[maxlag+lag3:len(sig)-(maxlag-lag3)]
    if(i==int(2*N/3)):
        m = np.linspace(0,length-2*maxlag-1,num=length-2*maxlag)
        plt.plot(m,data[:,0],m,data[:,1],m,data[:,2])
        plt.show()
    
    
    thetaestimates[i] = calculate_distance(data,i)

plt.plot(ns,thetas*180/np.pi, ns,thetaestimates*180/np.pi)
plt.legend(("Real angle","Estimated angle"))
print(thetaestimates[20]*180/np.pi)
    
    