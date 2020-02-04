# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:04:34 2020

@author: Vegard


Detect dominant frequency and band pass filter around that freq
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def detectDom(data, Ts, channel):
    nyq = 0.5/Ts
    x = data[:,channel]
    w = np.fft.fft(x)
    M = len(w)
    peakfreq = (np.argmax(abs(w[int(len(w)/2):]))+int(len(w)/2))*nyq/M
    """lag = 0
    while(freqs[lag+peakind] < 50):
        lag += peakind+1
        peakind = np.argmax(abs(w[lag:]))"""
    
    """if(freqs[peakind] > nyq):
        return False"""
    return peakfreq,x,len(w)
    

def butterBandpassFilter(data, Ts, channel, order=2):
    fc,x,M = detectDom(data,Ts,channel)
    nyq = 0.5/Ts
    lowcut = fc-0.01*nyq
    highcut = fc+0.01*nyq
    low = 1-lowcut/nyq
    high = 1-highcut/nyq
    print(low)
    print(high)
    soslow = signal.butter(order,low, btype='low', output='sos')
    soshigh = signal.butter(order,high, btype='high', output='sos')
    y = signal.sosfilt(soshigh, signal.sosfilt(soslow,x))
    plt.plot(data[:100,0])
    plt.plot(y[:100])
    plt.legend(("pure","filtered"))
    plt.show()
    
    z = np.abs(np.fft.fft(data[:,0]))
    w = np.abs(np.fft.fft(y))
    N = len(z)
    n = np.linspace(0, 0.5, int(N/2))
    plt.plot(n, z[:int(N/2)])
    plt.plot(n, w[:int(N/2)]*np.linalg.norm(z)/np.linalg.norm(w))
    plt.legend(("pure","filtered"))
    plt.show()
    return y
    
    
"""
N = 50
Ts = 1/3e5
data = np.zeros((N,2))
n = np.linspace(0,N-1,N)
data[:,0] = 0.5*np.sin(n/2) + np.sin(2*n/2) + 0.5*np.sin(3*n/2) + np.random.normal(0,0.5,N)
y = butterBandpassFilter(data,Ts,0)
plt.plot(data[:50,0])
plt.plot(y[:50])
plt.legend(("pure","filtered"))
plt.show()

z = np.abs(np.fft.fft(data[:,0]))
w = np.abs(np.fft.fft(y))

plt.plot(n/N, z)
plt.plot(n/N, w*np.linalg.norm(z)/np.linalg.norm(w))
plt.legend(("pure","filtered"))
plt.show()"""
    
    
    