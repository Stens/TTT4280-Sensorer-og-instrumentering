# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:45:48 2020

@author: Vegard

Function calcAngle(data)
calculate angle to sound source using cross corrolation on 3 channels(microphones)

Function calcAngleWithPlot(data)
also plots cross corrolations.

data is an array with dimensions NSAMPLES x NCHANNELS, only 3 first channels used
"""

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt


def preProc(data, upSampleFactor=1):
    length = len(data[:,0])
    mic = np.zeros((length,3))
    mic = signal.detrend(data[:,:3], axis=0, type="constant")
    
    if(upSampleFactor != 1):
        mic = signal.resample(mic, upSampleFactor*length, axis=0)
    
    # Might also add filter here
    
    return mic

def lagToAngle(maxLag):
    xish = (-1/2*maxLag[0] + 1/2*maxLag[1] + maxLag[2])
    b = xish < 0
    a = maxLag[0] - maxLag[1] - 2*maxLag[2]
    if(a != 0):
        theta = np.arctan(np.sqrt(3) * ((maxLag[0]+ maxLag[2])/a)) + b*np.pi
    else:
        theta = 0
    # Should be more elegant
    while(theta > np.pi/2):
        theta -= np.pi/2
    while(theta < -np.pi/2):
        theta += np.pi/2

    return -theta

def calcAngle(data):
    
    # Seperate the three mics and remove DC
    mic1 = signal.detrend(data[:,0], type="constant") 
    mic2 = signal.detrend(data[:,1], type="constant")
    mic3 = signal.detrend(data[:,2], type="constant")

    length = len(mic1) # Get length of samples

    # Crosscorrelation
    xcorr21 = np.correlate(mic1, mic2, "full")
    xcorr31 = np.correlate(mic1, mic3, "full")
    xcorr32 = np.correlate(mic2, mic3, "full")

    # Get max lag
    maxlag21 = np.argmax(xcorr21) - length
    maxlag31 = np.argmax(xcorr31) - length
    maxlag32  = np.argmax(xcorr32) - length

    # Calculate angles cool way B-)
    xish = (-1/2*maxlag21 + 1/2*maxlag31 + maxlag32)
    b = xish < 0
    if(maxlag21-maxlag31 -2*maxlag32 != 0):
        theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    else:
        theta = 0
    # Should be more elegant
    while(theta > np.pi/2):
        theta -= np.pi

    return -theta


def calcAngleWithPlot(data):
    
    # Seperate the three mics and remove DC
    mic1 = signal.detrend(data[:,0], type="constant") 
    mic2 = signal.detrend(data[:,1], type="constant")
    mic3 = signal.detrend(data[:,2], type="constant")

    length = len(mic1) # Get length of samples

    # Crosscorrelation
    xcorr21 = np.correlate(mic1, mic2, "full")
    xcorr31 = np.correlate(mic1, mic3, "full")
    xcorr32 = np.correlate(mic2, mic3, "full")
    
    # Plot Crosscorrolation
    plt.plot(xcorr21)
    plt.plot(xcorr31)
    plt.plot(xcorr32)
    plt.legend(("xcorr21","xcorr31","xcorr32"))
    plt.title("Cross corrolations")
    plt.xlabel("Sample")
    plt.show()

    # Get max lag
    maxlag21 = np.argmax(xcorr21) - length
    maxlag31 = np.argmax(xcorr31) - length
    maxlag32  = np.argmax(xcorr32) - length
    
    print("Lags: ")
    print(maxlag21)
    print(maxlag31)
    print(maxlag32)
    

    # Calculate angles cool way B-)
    xish = (-1/2*maxlag21 + 1/2*maxlag31 + maxlag32)
    b = xish < 0
    if(maxlag21-maxlag31 -2*maxlag32 != 0):
        theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    else:
        theta = 0
    # Should be more elegant
    while(theta > np.pi/2):
        theta -= np.pi

    return -theta

def myDot(x,y,l):
    r = 0
    if(l>0):
        x = x[:len(x)-l]
        y = y[l:]
        for i in range(len(x)):
            r += x[i]*y[i]
    else:
        x = x[-l:]
        y = y[:len(y)+l]
        for i in range(len(x)):
            r += x[i]*y[i]
    return r



def calcAngleEfficient(data, Fs, dist, c, sampleFactor=1):
    
    mic = preProc(data, sampleFactor)
    
    # Crosscorrelation
    lmax = int(np.ceil(1.5*Fs*sampleFactor*dist/c))
    xcorr = np.zeros((2*lmax+1,3))
    for l in range(-lmax, lmax+1):
        xcorr[lmax+l,0] = myDot(mic[:,0],mic[:,1],l)
        xcorr[lmax+l,1] = myDot(mic[:,0],mic[:,2],l)
        xcorr[lmax+l,2] = myDot(mic[:,1],mic[:,2],l)

    # Get max lag    
    maxLag = np.argmax(xcorr, axis=0) - np.ones(3)*lmax

    return lagToAngle(maxLag)

def calcAngleWithPlotEfficient(data, Fs, dist, c, sampleFactor=1):
    
    mic = preProc(data, sampleFactor)
    
    # Crosscorrelation
    lmax = int(np.ceil(Fs*sampleFactor*dist/c))
    xcorr = np.zeros((2*lmax+1,3))
    for l in range(-lmax, lmax+1):
        xcorr[lmax+l,0] = myDot(mic[:,0],mic[:,1],l)
        xcorr[lmax+l,1] = myDot(mic[:,0],mic[:,2],l)
        xcorr[lmax+l,2] = myDot(mic[:,1],mic[:,2],l)
    
    # Plot Crosscorrolation
    for i in range(3):
        plt.plot(range(-lmax, lmax+1), np.abs(xcorr[:,i]))
    plt.legend(("xcorr21","xcorr31","xcorr32"))
    plt.title("Cross corrolations")
    plt.xlabel("Lag")
    plt.show()

    # Get max lag    
    maxLag = np.argmax(xcorr, axis=0) - np.ones(3)*lmax
    
    print("Lags: ")
    print(maxLag[0])
    print(maxLag[1])
    print(maxLag[2])

    return lagToAngle(maxLag)
