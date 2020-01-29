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
    theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    
    # Should be more elegant
    while(theta > np.pi/2):
        theta -= np.pi

    return -theta

import matplotlib.pyplot as plt

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

    # Get max lag
    maxlag21 = np.argmax(xcorr21) - length
    maxlag31 = np.argmax(xcorr31) - length
    maxlag32  = np.argmax(xcorr32) - length

    # Calculate angles cool way B-)
    xish = (-1/2*maxlag21 + 1/2*maxlag31 + maxlag32)
    b = xish < 0
    theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    
    # Should be more elegant
    while(theta > np.pi/2):
        theta -= np.pi

    return -theta

def myDot(x,y,l):
    r = 0
    if(l>0):
        x = x[:len(x)-l]
        y = y[l:]
        r = np.dot(x,y)
    else:
        x = x[l:]
        y = y[:len(y)-l]
    return r

def calcAngleEfficient(data, Fs, dist, c):
    
    # Seperate the three mics and remove DC
    mic1 = signal.detrend(data[:,0], type="constant") 
    mic2 = signal.detrend(data[:,1], type="constant")
    mic3 = signal.detrend(data[:,2], type="constant")

    # Crosscorrelation
    lmax = int(np.ceil(Fs*dist/c))
    xcorr = np.zeros((2*lmax+1,3))
    for l in range(-lmax, lmax+1):
        xcorr[:,0] = myDot(mic1,mic2,l)
        xcorr[:,1] = myDot(mic1,mic3,l)
        xcorr[:,2] = myDot(mic2,mic3,l)

    # Get max lag
    maxlag21 = np.argmax(xcorr[:,0]) - lmax
    maxlag31 = np.argmax(xcorr[:,1]) - lmax
    maxlag32  = np.argmax(xcorr[:,2]) - lmax

    # Calculate angles cool way B-)
    xish = (-1/2*maxlag21 + 1/2*maxlag31 + maxlag32)
    b = xish < 0
    theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    
    # Should be more elegant
    while(theta > np.pi/2):
        theta -= np.pi

    return -theta

def calcAngleWithPlotEfficient(data, Fs, dist, c):
    
    # Seperate the three mics and remove DC
    mic1 = signal.detrend(data[:,0], type="constant") 
    mic2 = signal.detrend(data[:,1], type="constant")
    mic3 = signal.detrend(data[:,2], type="constant")

    # Crosscorrelation
    #xcorr21 = np.correlate(mic1, mic2, "full")
    #xcorr31 = np.correlate(mic1, mic3, "full")
    #xcorr32 = np.correlate(mic2, mic3, "full")
    lmax = int(np.ceil(Fs*dist/c))
    xcorr = np.zeros((2*lmax+1,3))
    for l in range(-lmax, lmax+1):
        xcorr[:,0] = myDot(mic1,mic2,l)
        xcorr[:,1] = myDot(mic1,mic3,l)
        xcorr[:,2] = myDot(mic2,mic3,l)
    
    # Plot Crosscorrolation
    for i in range(3):
        plt.plot(xcorr[:,i])
    plt.legend(("xcorr21","xcorr31","xcorr32"))
    plt.title("Cross corrolations")
    plt.xlabel("Sample")

    # Get max lag
    maxlag21 = np.argmax(xcorr[:,0]) - lmax
    maxlag31 = np.argmax(xcorr[:,1]) - lmax
    maxlag32  = np.argmax(xcorr[:,2]) - lmax

    # Calculate angles cool way B-)
    xish = (-1/2*maxlag21 + 1/2*maxlag31 + maxlag32)
    b = xish < 0
    theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    
    # Should be more elegant
    while(theta > np.pi/2):
        theta -= np.pi

    return -theta
