# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:13:34 2020

@author: Vegard
"""

import numpy as np


def measureSpeed(data,Fs,realChannel,imagChannel,f0=24.13e9):
    fft,freqs = complexFFT(data,Fs,realChannel,imagChannel)
    peakFreq = findPeak(fft,freqs)
    speed = dopplerFormula(peakFreq)
    return speed

def complexFFT(data,Fs,realChannel,imagChannel):
    IFI = data[:,imagChannel]
    IFQ = data[:,realChannel]
    IF = IFI + 1j*IFQ
    fft = np.fft(IF) ##Maybe need to ditch first few samples because shit samples
    N = len(fft)
    freqs = np.linspace(0,Fs,N) ## Kanskje ikke rett
    return fft,freqs

def findPeak(fft,freqs):
    i = np.argmax(fft)
    peakFreq = freqs[i]
    return peakFreq

def dopplerFormula(fd, f0=24.13e9):
    c=3e8
    v=c*fd/2/f0
    return v

