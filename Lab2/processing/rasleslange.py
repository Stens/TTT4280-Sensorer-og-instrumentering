# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:06:15 2020

@author: Vegard
"""

import xcorr
import numpy as np

d = 0.07
c = 343
Ts, data = xcorr.raspi_import("adcData.bin")

thetaefffilter2 = xcorr.calcAngleWithPlotEfficient(data,1e6/Ts,d,c,3,3)
print("Small boi filtered xcorr with 2xupsampling gives {} degrees".format(thetaefffilter2*180/np.pi))

