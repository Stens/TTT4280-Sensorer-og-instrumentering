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
    return data # Return only the data


def preProc(data, Ts, upSampleFactor=1, filterorder=0):
    length = len(data[:,0])
    mic = np.zeros((length,3))
    mic = signal.detrend(data[:,:3], axis=0, type="constant")
    if(filterorder > 0):
        for i in range(3):
            mic[:,i] = bandpass.butterBandpassFilter(mic,Ts,i,filterorder)
    
    if(upSampleFactor != 1):
        mic = signal.resample(mic, upSampleFactor*length, axis=0)
    
    # Might also add filter here

    
    return mic

def lagToAngle(maxLag):
    xish = (-1/2*maxLag[0] + 1/2*maxLag[1] + maxLag[2])
    b = xish < 0
    a = maxLag[0] - maxLag[1] - 2*maxLag[2]
    if(a != 0):
        theta = np.arctan(np.sqrt(3) * ((maxLag[0]+ maxLag[1])/a)) #+ b*np.pi
    else:
        theta = 0
    # Should be more elegant
    """while(theta > np.pi/2):
        theta -= np.pi/2
    while(theta < -np.pi/2):
        theta += np.pi/2"""

    return theta

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



def calcAngleEfficient(data, Fs, dist, c, sampleFactor=1,filterorder=0):
    
    mic = preProc(data, 1e6/Fs,sampleFactor, filterorder)
    
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
    
    mic = preProc(data, 1e6/Fs, sampleFactor, filterorder)
    
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


def circularPLot(theta):
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    # ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*3, color='r', linestyle='-')
    N = 4
    width = 2*np.pi/N
    for i in range(N):
        ax.bar((i*width)+np.pi/2,2, width=width, bottom=1.5, alpha=0.3)
    ax.bar(theta, 4, width=np.pi/36, bottom=0.0, alpha=0.7)
    circle1 = plt.Circle((0.0, 1.0), 0.2, transform=ax.transData._b, color="red", alpha=0.4)
    circle2 = plt.Circle((1.0, -1.0), 0.2, transform=ax.transData._b, color="red", alpha=0.4)
    circle3 = plt.Circle((-1.0, -1.0), 0.2, transform=ax.transData._b, color="red", alpha=0.4)

    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)
    # ax.set_theta_zero_location("N")

    plt.yticks([], [])
    plt.show()

circularPLot(1)
def approval():
    N_files = 11
    files = {}

    for i in range (N_files):
        files["file"+str(i+1)] = raspi_import("../measurements/adcData"+str(i+1)+".bin")

    # for i in range(3):

    #     plt.title("Filtered sound "+str(i+1))
    #     plt.show()
        
    plt.plot(files["file11"][10:,0])
    plt.show()

    # for i in range(3):
    #     data = files["file"+str(i+1)]
    #     mic1 = signal.detrend(data[:,0], type="constant") 
    #     mic2 = signal.detrend(data[:,1], type="constant")
    #     mic3 = signal.detrend(data[:,2], type="constant")


    #     # Crosscorrelation
    #     xcorr21 = np.correlate(mic1, mic2, "full")
    #     # xcorr31 = np.correlate(mic1, mic3, "full")
    #     # xcorr32 = np.correlate(mic2, mic3, "full")
    #     plt.plot(xcorr21)
    #     plt.title("Cross corrolation "+str(i+1))
    #     plt.xlabel("Lag")
    #     plt.show()


    # for i in range(N_files):
    #     circularPLot(calcAngleEfficient(files["file"+str(i+1)], 33000, 6.3, 343, sampleFactor=1))





# After talking with Peter Uran, and Peter Svensson we have decided on the following requirements that must be fulfilled for passing Lab 2, the acoustics lab.

# 1) We need to see plots of three time signals of the sampled sounds from the microphone which have been filtered of some sorts.

# 2) We need to see three cross-correlation-plots zoomed in on zero, so we can see the lag that is indicated by the highest peak.

# 3) We need to see ten estimations of angles, evenly distributed over the four quadrants. Preferably in a circle plot which shows where on the circle the angles are.

# 4) Finally, give a table with three coloumns, and ten rows where each row corresponds to one of the estimated angles from 3). Each row should have these numbers: Estimated angle, actual angle and deviation (avvik) of the angle-estimate from the true angle.

# import matplotlib.animation as animation
# ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
# plt.show()