# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:06:15 2020

@author: Vegard
"""

import xcorr
import import_data
import numpy as np



d = 0.07
c = 343


Ts, data = import_data.raspi_import("adcData.bin")


thetafull = xcorr.calcAngleWithPlot(data)
#thetaeff = xcorr.calcAngleWithPlotEfficient(data,1e6/Ts,d,c)
thetaeff2 = xcorr.calcAngleWithPlotEfficient(data,1e6/Ts,d,c,2)
#thetaefffilter = xcorr.calcAngleWithPlotEfficient(data,1e6/Ts,d,c,1,4)
thetaefffilter2 = xcorr.calcAngleWithPlotEfficient(data,1e6/Ts,d,c,2,2)



print("Full xcorr gives {} degrees".format(thetafull*180/np.pi))
#print("Small boi xcorr gives {} degrees".format(thetaeff*180/np.pi))
print("Small boi xcorr with 2xupsampling gives {} degrees".format(thetaeff2*180/np.pi))
#print("Small boi filtered xcorr gives {} degrees".format(thetaefffilter*180/np.pi))
print("Small boi filtered xcorr with 2xupsampling gives {} degrees".format(thetaefffilter2*180/np.pi))


## Plot the shit
#import_data.plotData(data,Ts,4096, range(3))
