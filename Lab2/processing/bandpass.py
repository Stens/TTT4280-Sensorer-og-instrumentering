# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:04:34 2020

@author: Vegard


Detect dominant frequency and band pass filter around that freq
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def detectDominantFreq(y,Ts):
    w = np.fft.fft(y)
    M = len(w)
    nyq = 0.5/Ts
    peakFreq = (np.argmax(abs(w[int(M/2):]))-int(M/2))*nyq/M
    return peakFreq


def butterBandPassFilter(data,Ts,channel,order=2):
    nyq = 0.5/Ts
    x = data[:,channel]
    
    lowcut = 500 #Hz Filter low freq
    low = lowcut/nyq
    b,a = signal.butter(order,low,btype='high',output='ba')
    y = signal.lfilter(b,a,x)
    f = abs(detectDominantFreq(y,Ts))
    highfc = (f + nyq)/2
    high = highfc/nyq
    b,a = signal.butter(order,high,btype='low',output='ba')
    z = signal.lfilter(b,a,y)
    return z
    

    
    