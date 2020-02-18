# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:45:48 2020

@author: Vegard

data is an array with dimensions NSAMPLES x NCHANNELS, only 3 first channels used
"""

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import bandpass

def raspi_import(path, channels=5):
    """
    Import data produced using adc_sampler.c.

    Parameters
    ----------
    path: str
        Path to file.
    channels: int, optional
        Number of channels in file.

    Returns
    -------
    sample_period: float
        Sample period
    data: ndarray, uint16
        Sampled data for each channel, in dimensions NUM_SAMPLES x NUM_CHANNELS.
    """

    with open(path, 'r') as fid:
        sample_period = np.fromfile(fid, count=1, dtype=float)[0]
        data = np.fromfile(fid, dtype=np.uint16)
        data = data.reshape((-1, channels))
    return sample_period,data 

def preProcessing(data, Ts, upSampleFactor=1, filterorder=0):
    length = len(data[10:,0])
    mic = np.zeros((length,3))
    adcs = [3,1,2]
    mic = signal.detrend(data[10:,adcs], axis=0, type="constant")
    if(filterorder > 0):
        for i in range(3):
            mic[:,i] = bandpass.butterBandPassFilter(mic,Ts,i,filterorder)
    
    if(upSampleFactor != 1):
        
        
        
        
        
        
        lso add filter here

    
    return mic

def lagToAngle(maxLag):
    xish = (-1/2*maxLag[0] + 1/2*maxLag[1] + maxLag[2])
    b = xish < 0
    a = maxLag[0] - maxLag[1] - 2*maxLag[2]
    if(a != 0):
        theta = np.arctan(np.sqrt(3) * ((maxLag[0]+ maxLag[1])/a)) + b*np.pi
    else:
        theta = 0
    if(theta < -np.pi):
        theta += 2*np.pi
    elif(theta > np.pi):
        theta -= 2*np.pi
    return theta


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



def calcAngleEfficient(data, Fs, dist, c, sampleFactor=1,filterorder=0):
    
    mic = preProcessing(data, 1/Fs,sampleFactor, filterorder)
    
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

def calcAngleWithPlotEfficient(data, Fs, dist, c, sampleFactor=1,filterorder=0):
    
    mic = preProcessing(data, 1/Fs, sampleFactor, filterorder)
    
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


def approval():
    N_files = 3
    files = {}

    for i in range (N_files):
        ts, files["file"+str(i+1)] = raspi_import("../measurements/adcData"+str(i+1)+".bin")

    for i in range(1):
        fil = files["file"+str(i+1)]
        unfiltered = preProcessing(fil,ts*(10**(-6)),upSampleFactor=10,filterorder=0)
        filtered = preProcessing(fil,ts*(10**(-6)),upSampleFactor=10,filterorder=3)
        plt.plot(filtered[:,0])
        plt.plot(unfiltered[:,0])
        plt.legend(("Filtered","Unfiltered"))
        plt.title("Filtered sound "+str(i+1))
        plt.show()
        
    
    for i in range(1):
        data = files["file"+str(i+1)]
        mic1 = signal.detrend(data[:,0], type="constant") 
        mic2 = signal.detrend(data[:,1], type="constant")
        mic3 = signal.detrend(data[:,2], type="constant")

        # Crosscorrelation
        xcorr21 = np.correlate(mic1, mic2, "full")
        xcorr31 = np.correlate(mic1, mic3, "full")
        xcorr32 = np.correlate(mic2, mic3, "full")
        plt.plot(xcorr21)
        plt.plot(xcorr31)
        plt.plot(xcorr32)
        plt.title("Cross corrolation "+str(i+1))
        plt.xlabel("Lag")
        plt.show()

#approval()