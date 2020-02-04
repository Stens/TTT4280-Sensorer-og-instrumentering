import socket
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import copy

HOST = '192.168.43.15'  # The rpi's hostname or IP address
PORT = 8080        # The port used by the server
MAX = 300
ARRAY_SIZE = int(MAX/2)
ADCS = 5 # Hardcoded on the pi

def stream_measurements():
    np_data_arr = np.zeros(10*MAX,dtype=np.uint16)
    i = 0
    send_string = "STREAM"
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        time.sleep(2)
        while True:
            # time.sleep(1)
            s.send(bytes(send_string,"utf-8")) # REC=Recording , STREAM=stream
            try:
                data = s.recv(MAX)
                shift(np_data_arr, ARRAY_SIZE, np.frombuffer(data, dtype=np.uint16,) )
                # timedomain_x = np.arange(0,0.033456,0.00003352304)
                # timedomain_y = [org_data[j]*0.00080566406 for j in range(ARRAY_SIZE)]
                # timedomain_y = timedomain_y[1:]
                i += 1
                if i > 100:
                    dat = np_data_arr.reshape((-1, 5))
                    org_data = dat[:,0]
                    plt.plot(org_data)
                    plt.show()
                    break
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
    

def do_stuff(arr):
    data = arr.reshape((-1, channels))
    org_data = data[:,0]
    timedomain_x = np.arange(0,0.033456,0.00003352304)
    timedomain_y = [org_data[j]*0.00080566406 for j in range(1000)]
    timedomain_y = timedomain_y[1:]
    plt.plot(timedomain_x, timedomain_y)
    plt.title("Sampling ADC " + str(0+1))
    plt.show()
    # fourier = (abs(sci.fft(timedomain_y)))
    # # plt.plot(20*np.log10(fourier))
    # plt.plot((fourier))

    # # plt.yscale("log")
    # plt.title("FFT ADC "  + str(i+1))
    # plt.show()


stream_measurements()
