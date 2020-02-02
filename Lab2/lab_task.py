import numpy as np 
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time

c = 343
d = 0.075
Fs = 31250
LAG_MAX = Fs * (d/c)

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
    return sample_period, data


def calculate_angle():
    start = time.time()
    # Get the three microphones
    [Ts, data] = raspi_import("./stens.bin")

    # Seperate the three mics and remove DC
    mic1 = signal.detrend(data[:,0], type="constant") 
    mic2 = signal.detrend(data[:,1], type="constant")
    mic3 = signal.detrend(data[:,2], type="constant")

    length = len(mic1) # Get length of samples

    # Crosscorrelation
    xcorr21 = np.absolute(np.correlate(mic1, mic2,mode="full"))
    xcorr31 = np.absolute(np.correlate(mic1, mic3,mode="full"),)
    xcorr32 = np.absolute(np.correlate(mic2, mic3,mode="full"))

    # Get max lag
    maxlag21 = np.argmax(xcorr21) - length
    maxlag31 = np.argmax(xcorr31) - length
    maxlag32  = np.argmax(xcorr32) - length


    # Calculate angle
    # Lame calculations
    # theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))

    # Calculate angles cool way B-)

    xish = (-1/2*maxlag21 + 1/2*maxlag31 + maxlag32)
    b = xish < 0
    theta = np.arctan(np.sqrt(3) * ((maxlag21+ maxlag31)/(maxlag21-maxlag31 -2*maxlag32))) + b*np.pi
    print(theta)

    





calculate_angle()    