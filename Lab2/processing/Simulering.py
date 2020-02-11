# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:20:57 2020

@author: Vegard
"""

import numpy as np
import matplotlib.pyplot as plt
import xcorr

  
    
K = 10

# Parameters
N = 200 # Num angles
c = 343 # Speed of Sound
d = 0.07 # Distance between mics
nF = 5
F = 3000 # Base frequency of signal
Fs = 31250 # Sample frequency
length = 500 # Num samples
M = 10 # Num harmonics in signal
L = 1 # Number of repetitions with different noise
mu = 0 # Mean of gaussian noise
sigma = 1 # Std of gaussian noise
samplingFactor = 2 # Seems to be good trade off between resolution and cost
order = 3 # Likely best filter order




thetas = np.linspace(-np.pi*150/180, np.pi*150/180, num=N)
thetaestimates = np.zeros(N)
thetaestimates1 = np.zeros(N)
thetaestimates2 = np.zeros(N)
thetaestimates5 = np.zeros(N)
 
ns=np.linspace(0,N-1,num=N)

#mse = np.zeros((nF,3))
maxlag = int(np.ceil(d/np.sqrt(3)/c*Fs))

n = np.linspace(0,(length-1),num=length)
sig = 0
for i in range(M+1):
    if(i > 0):
        sig += np.sin(i*n*F/Fs)
    sig += np.sin(i*n*F/Fs)
sig /= M

mse = np.zeros(K)



for i in range(N):
    data = np.zeros((length-2*maxlag,5))
    lag1 = int(maxlag*np.cos(thetas[i]-np.pi/2))
    lag2 = int(maxlag*np.cos(thetas[i]+30*np.pi/180))
    lag3 = int(maxlag*np.cos(thetas[i]+150*np.pi/180))
    
    data[:,3] = sig[maxlag+lag1:len(sig)-(maxlag-lag1)]
    data[:,1] = sig[maxlag+lag2:len(sig)-(maxlag-lag2)] 
    data[:,2] = sig[maxlag+lag3:len(sig)-(maxlag-lag3)]
    
    v = [3,2,1]
    for j in v:
        data[:,j] += np.random.normal(mu, sigma, length-2*maxlag)
        
    if(i == int(N*2/3)):
        plt.plot(data[:,3])
        plt.plot(data[:,1])
        plt.plot(data[:,2])
        plt.legend(("Mic 1", "Mic 2", "Mic 3"))
        plt.title("Time domain. sigma = {}, theta = {}".format(sigma,np.round(thetas[i])))
        plt.show()
    
    thetaestimates[i] = xcorr.calcAngleEfficient(data, Fs,d,c,samplingFactor,order)
    #thetaestimates1[i] = -xcorr.calcAngleEfficient(data, Fs, d, c, 2,2)
    #thetaestimates2[i] = -xcorr.calcAngleEfficient(data, Fs, d, c, 2,4)


"""
plt.plot(sigmas,mse)
plt.title("MSE for different noise std, order 3, 2x upsampling")
plt.xlabel("Standard deviation sigma")
plt.ylabel("MSE")
plt.savefig("SimulateNoise.jpg",quality=95,dpi=1500)
plt.show()"""




plt.plot(thetas*180/np.pi,thetas*180/np.pi, thetas*180/np.pi,thetaestimates*180/np.pi)
plt.legend(("Real angle","short xcorr 2x filter order 3"))
plt.title("Estimated angle")
plt.ylabel("Estimated theta")
plt.xlabel("Real theta")
plt.savefig("SimAngle4.jpg",quality=95,dpi=1000)
plt.show()

mae = np.mean(np.abs(thetas-thetaestimates))*180/np.pi
print("Mean Absolute Error: {} degrees".format(np.round(mae,decimals=1)))

snr = np.mean(sig**2)/sigma**2
print("Signal to Noise Ratio: {} ".format(np.round(snr,decimals=1)))




    