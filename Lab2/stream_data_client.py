import socket
import numpy as np

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080        # The port used by the server
HEADERSIZE = 20     # The length of the header
MAX = 1024
ADCS = 5 # Hardcoded on the pi


def get_measurements(num_samples): 

    not_done = True
    total_datapoints = ADCS*num_samples + (ADCS*MAX-ADCS*num_samples)
    full_data = np.zeros(total_datapoints)
    i = 0
    stop = ADCS*MAX
    cleaned_data = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(bytes("R"+" "+str(num_samples),"utf-8") # R=Recording , S=stream 

        while not_done:

            data = s.recv(MAX)
           
            full_data[i:i+MAX] += data
            i+=1

            if i == stop:
                not_done = False

        s.send(bytes("exit"),"utf-8")
    print("Received measurements")
    cleaned_data = full_data[:ADCS*num_samples]
    return cleaned_data 

def write_msg_to_file(filename, msg);
    f = open("./measurements/"+ filename, 'wb')
    f.write(msg)
    f.close()




