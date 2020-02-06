import socket
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
from threading import Thread
import xcorr

HOST = '192.168.43.15'  # The rpi's hostname or IP address
PORT = 8080        # The port used by the server
MAX = 300
ARRAY_SIZE = int(MAX/2)
ADCS = 5 # Hardcoded on the pi
np_data_arr = np.zeros(30*MAX,dtype=np.uint16)
fig = plt.figure()
ax1 = fig.add_subplot(111, polar=True)


def show_sine(i):
    ax1.clear()
    dat = np_data_arr.reshape((-1, 5))
    org_data = dat[:,0]
    ax1.plot(org_data)

def show_direction(i):
    ax1.clear()
    dat = np_data_arr.reshape((-1, 5))
    theta = xcorr.calcAngleEfficient(dat,33000,0.07,343,filterorder=3,sampleFactor=1)
    N = 4
    width = 2*np.pi/N
    for i in range(N):
        ax1.bar(i*width,3, width=width, bottom=1.0, alpha=0.3)
    ax1.bar(theta, 4, width=np.pi/18, bottom=0.0, alpha=0.7)
    circle1 = plt.Circle((0.0, 1.0), 0.2, transform=ax1.transData._b, color="red", alpha=0.4)
    circle2 = plt.Circle((1.0, -1.0), 0.2, transform=ax1.transData._b, color="red", alpha=0.4)
    circle3 = plt.Circle((-1.0, -1.0), 0.2, transform=ax1.transData._b, color="red", alpha=0.4)
    print(np.round(theta*180/np.pi,0))
    ax1.tick_params(
    axis='y',          
    which='both',      
    bottom=False,
    top=False,         
    labelbottom=False) 

    ax1.add_artist(circle1)
    ax1.add_artist(circle2)
    ax1.add_artist(circle3)


def stream_measurements():
    i = 0
    send_string = "STREAM"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        time.sleep(2)
        while True:
            s.send(bytes(send_string,"utf-8")) # REC=Recording , STREAM=stream
            try:
                data = s.recv(MAX)
                shift(np_data_arr, ARRAY_SIZE, np.frombuffer(data, dtype=np.uint16,) )
            except Exception as e:
                print("noe gikk galt" +str(e))  



# Helper function
def shift(arr, num, fill_value=np.nan):
    if num > 0:
        arr[:num] = fill_value
        arr[num:] = arr[:-num]
    elif num < 0:
        arr[num:] = fill_value
        arr[:num] = arr[-num:]


# Start streaming values on separate thread
stream = Thread(target = stream_measurements, args = (),)
stream.start()

# Plot showing direction, updates every 100ms
ani = animation.FuncAnimation(fig, show_direction, interval=100)
plt.show()