#include <stdio.h> 
#include <netdb.h> 
#include <netinet/in.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <pthread.h>
#include <unistd.h>
#include "adc.h"
#include "stream_data_server.h"


void sendData(int sockfd) 
{ 
	char buff[MAX]; 
    int num_samples;
    char *pEnd;
	int data_chunks;	
	int wid;
	int done = 0;
	rawWaveInfo_t rwi = initADC(&wid);
    uint16_t *stream_vals = (uint16_t*)malloc(sizeof(uint16_t)*NUM_STREAM_SAMPLES*ADCS);


	while (1) { 
		bzero(buff, MAX); 

		// read the message from client and copy it in buffer 
		read(sockfd, buff, sizeof(buff)); 
        if (!strncmp("REC", buff, 3)) { // Not tested fully
			
			strncpy(buff, buff+4, 4);
			memset(buff+4,'\0',4);
            num_samples = strtol(buff,&pEnd,10);
			uint16_t *read_val = (uint16_t*)malloc(sizeof(uint16_t)*num_samples*ADCS);

			readADC(rwi, wid, sockfd, done, num_samples ,stream_vals);
			
			bzero(buff, MAX); 
			data_chunks = (ADCS*num_samples + (MAX / 2)) / MAX;
			printf("%d data chunks\n", data_chunks);

			// and send vals to client 
			for (size_t i = 0; i <= data_chunks; i++)
			{
				write(buff, read_val+(i*sizeof(uint16_t)*NUM_STREAM_SAMPLES*ADCS), 
				sizeof(uint16_t)*NUM_STREAM_SAMPLES*ADCS);	 
			}
			free(read_val);
			done = 1;
        }

		else if (!strncmp("STREAM", buff, 6)) 
		{

			// and send vals to client 
			readADC(rwi, wid, sockfd, done, NUM_STREAM_SAMPLES ,stream_vals);
			write(sockfd, stream_vals, sizeof(uint16_t)*NUM_STREAM_SAMPLES*ADCS); // = MAX = 300 ??
			done = 1;

		}
		
		// if msg contains "Exit" then server exit and chat ended. 
		else  { 
			printf("Server Exit...\n"); 
			gpioTerminate();
			free(stream_vals);
			break; 
		} 
	} 
} 


// main init function. Starts the server
int main() 
{ 
	int sockfd, connfd, len; 
	struct sockaddr_in servaddr, cli; 

	// socket create and verification 
	sockfd = socket(AF_INET, SOCK_STREAM, 0); 
	if (sockfd == -1) { 
		printf("socket creation failed...\n"); 
		exit(0); 
	} 
	else
		printf("Socket successfully created..\n"); 
	bzero(&servaddr, sizeof(servaddr)); 

	// assign IP, PORT 
	servaddr.sin_family = AF_INET; 
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
	servaddr.sin_port = htons(PORT); 

	// Binding newly created socket to given IP and verification 
	if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) { 
		printf("socket bind failed...\n"); 
		exit(0); 
	} 
	else
		printf("Socket successfully binded..\n"); 

	// Now server is ready to listen and verification 
	if ((listen(sockfd, 5)) != 0) { 
		printf("Listen failed...\n"); 
		exit(0); 
	} 
	else
		printf("Server listening..\n"); 
	len = sizeof(cli); 

	// Accept the data packet from client and verification 
	connfd = accept(sockfd, (SA*)&cli, &len); 
	if (connfd < 0) { 
		printf("server acccept failed...\n"); 
		exit(0); 
	} 
	else
		printf("server acccept the client...\n"); 

	// Function for sending data
	sendData(connfd); 

	// Transaction complete, close the socket
	close(sockfd); 
} 
