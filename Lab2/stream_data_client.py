#

import socket
import numpy as np
import sys


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server
HEADERSIZE = 20     # The length of the header
MAX = 1024
ADCS = 5 # Hardcoded on the pi
FILENAME = "adcData"


def get_measurements(num_samples): 

    not_done = True
    total_datapoints = ADCS*num_samples + (ADCS*MAX-ADCS*num_samples)
    i = 0
    stop = ADCS*MAX
    full_data = ''
    cleaned_data = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(bytes("R"+" "+str(num_samples),"utf-8")) # R=Recording , S=stream 

        while not_done:

            data = s.recv(MAX)
           
            full_data = data
            i+=1

            if i == stop:
                not_done = False

        s.send(bytes(("exit"),"utf-8"))
    print("Received measurements")
    return full_data[:ADCS*num_samples]
      




def write_data_to_file(filename, bin_data):
    f = open("./measurements/"+ filename+".bin", 'wb')
    f.write(bin_data)
    f.close()


def stream_measurements(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            s.send(bytes("STREAM","utf-8") # R=Recording , S=stream
            data = s.recv(MAX)
            



if len(sys.argv) == 1:
    bin_data = get_measurements(1000)
    write_data_to_file(FILENAME, bin_data)
elif  len(sys.argv) == 2:
    bin_data = get_measurements(int(sys.argv[1]))
    write_data_to_file(FILENAME, bin_data)


elif len(sys.argv) == 3:
    for i in range(int(sys.argv[2]))
        bin_data = get_measurements(int(sys.argv[1]))
        write_data_to_file(FILENAME + str(i+1), bin_data)







