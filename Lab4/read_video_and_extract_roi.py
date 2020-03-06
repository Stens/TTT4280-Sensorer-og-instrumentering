"""
Read the input video file, display first frame and ask the user to select a
region of interest.  Will then calculate the mean of each frame within the ROI,
and return the means of each frame, for each color channel, which is written to
file.

Similar to read_video_and_extract_roi.m, but for Python.

Requirements:

* Probably ffmpeg. Install it through your package manager.
* numpy
* OpenCV python package.
    For some reason, the default packages in Debian/Raspian (python-opencv and
    python3-opencv) seem to miss some important features (selectROI not present
    in python3 package, python2.7 package not compiled with FFMPEG support), so
    install them (locally for your user) using pip:
    - pip install opencv-python
    - (or pip3 install opencv-python)
"""
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def extract_vals(filename):
    #read video file
    cap = cv2.VideoCapture(filename, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Could not open input file. Wrong filename, or your OpenCV package might not be built with FFMPEG support. See docstring of this Python script.")
        exit()

    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    mean_signal = np.zeros((num_frames, 3))

    #loop through the video
    count = 0
    while cap.isOpened():
        ret, frame = cap.read() #'frame' is a normal numpy array of dimensions [height, width, 3], in order BGR
        if not ret:
            break

        #display window for selection of ROI
        if count == 0:
            cv2.namedWindow("Image",2)
            window_text = 'Select ROI by dragging the mouse, and press SPACE or ENTER once satisfied.'
            ROI = cv2.selectROI("Image", frame) #ROI contains: [x, y, w, h] for selected rectangle
            cv2.destroyWindow("Image")
            print("Looping through video.")

        #calculate mean
        cropped_frame = frame[ROI[1]:ROI[1] + ROI[3], ROI[0]:ROI[0] + ROI[2], :]
        mean_signal[count, :] = np.mean(cropped_frame, axis=(0,1))
        count = count + 1

    cap.release()

    return mean_signal, fps


def find_heartbeat(data, fps):
    width = 25
    labels = ["Blue", "Green", "Red"]
    fps = 40
    for chan in range(data.shape[1]):
        channel = data[:,chan]
        snr = signaltonoise(channel)
        print("SNR before: "+str(snr))
        channel = signal.detrend(channel, type="constant")
        channel = channel[width-1:] - moving_average(channel, width)

        freqs = np.fft.fftfreq(len(channel),1/fps)
        spectrum = np.fft.fft(channel, len(channel))
        spectrum = np.fft.fftshift(spectrum)
        freqs = np.fft.fftshift(freqs)
        # freqs = np.linspace(0,len(spectrum)*steps,len(spectrum)*steps)
        plt.plot(channel)
        plt.title(labels[chan])
        plt.show()
        plt.plot(freqs, abs(10*np.log10((spectrum))))
        plt.title(labels[chan])

        plt.show()
        peakfreq = np.argmax(abs(spectrum))
        pulse = abs(freqs[peakfreq])*60
        snr = signaltonoise(channel)
        print("SNR after: " +str(snr))
        print("Pulse: "+ str(pulse) + "bpm")

    


#CLI options
if len(sys.argv) < 2:
    print("Select smaller ROI of a video file, and save the mean of each image channel to file, one column per color channel (R, G, B), each row corresponding to a video frame number.")
    print("")
    print("Usage:\npython " + sys.argv[0] + " [path to input video file] [path to output data file]")
    exit()
filename = sys.argv[1]

dat , fps=  extract_vals(filename)
find_heartbeat(dat, fps)