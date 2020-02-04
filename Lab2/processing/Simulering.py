# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:20:57 2020

@author: Vegard
"""

import numpy as np
import matplotlib.pyplot as plt
import xcorr

  
    
## Generate some shiiit

# Parameters
N = 100 # Num angles
c = 343 # Speed of Sound
d = 0.07 # Distance between mics
nF = 5
F = np.linspace(20, 20000, num=nF) # Base frequency of signal
Fs = 31250 # Sample frequency
length = 100 # Num samples
M = 1 # Num harmonics in signal
L = 1 # Number of repetitions with different noise
mu = 0 # Mean of gaussian noise
sigma = 0.5 # Std of gaussian noise


thetas = np.linspace(-np.pi/2.2, np.pi/2.2, num=N)
thetaestimates = np.zeros(N)
thetaestimates1 = np.zeros(N)
thetaestimates2 = np.zeros(N)
thetaestimates5 = np.zeros(N)
 
ns=np.linspace(0,N-1,num=N)

mse = np.zeros((nF,3))
maxlag = int(np.ceil(d/np.sqrt(3)/c*Fs))

for f in range(nF):
    
    # Signal generation
    n = np.linspace(0,(length-1)/3, num=length)
    sig = 0
    for i in range(M+1):
        sig += np.sin(i*n*F[f]/Fs)
    sig /= M
        
    
    
    

    for i in range(N):
        data = np.zeros((length-2*maxlag,3))
        lag1 = int(maxlag*np.cos(thetas[i]-np.pi/2))
        lag2 = int(maxlag*np.cos(thetas[i]+30*np.pi/180))
        lag3 = int(maxlag*np.cos(thetas[i]+150*np.pi/180))
        
        data[:,0] = sig[maxlag+lag1:len(sig)-(maxlag-lag1)]
        data[:,1] = sig[maxlag+lag2:len(sig)-(maxlag-lag2)] 
        data[:,2] = sig[maxlag+lag3:len(sig)-(maxlag-lag3)]
        for j in range(3):
            data[:,j] += np.random.normal(mu, sigma, length-2*maxlag)
        if(i==int(2*N/3)):
            m = np.linspace(0,length-2*maxlag-1,num=length-2*maxlag)
            plt.plot(m,data[:,0],m,data[:,1],m,data[:,2])
            plt.show()
            xcorr.calcAngleWithPlotEfficient(data,Fs,d,c)
            xcorr.calcAngleWithPlot(data)
        
        
        thetaestimates[i] = xcorr.calcAngle(data)
        thetaestimates1[i] = xcorr.calcAngleEfficient(data, Fs, d, c, 1)
        thetaestimates2[i] = xcorr.calcAngleEfficient(data, Fs, d, c, 2)
        mse[f,0] += (thetas[i]-thetaestimates[i])**2
        mse[f,1] += (thetas[i]-thetaestimates1[i])**2
        mse[f,2] += (thetas[i]-thetaestimates2[i])**2
    if(f%5==0):
        print("Iteration {} done".format(f))
    

plt.plot(ns,thetas*180/np.pi, ns,thetaestimates*180/np.pi, ns,thetaestimates1*180/np.pi, ns,thetaestimates2*180/np.pi)
plt.legend(("Real angle","Estimated angle", "New Estimate", "2xsampling"))
plt.show()

mse = np.sqrt(mse/N)*180/np.pi

plt.plot(F, mse[:,0], F, mse[:,1], F, mse[:,2])
plt.legend(("full", "partial", "2xsampling part"))
plt.xlabel("Frequency [Hz]")
plt.ylabel("MSE")
plt.title("MSE for different methods") 

    