#include <stdio.h> 
#include <netdb.h> 
#include <netinet/in.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <pthread.h>
#include "adc.h"
#include "stream_data_server.h"


void sendData(int sockfd) 
{ 
	char buff[MAX]; 
    int num_samples;
    char *pEnd;
	int data_chunks;	

	while (1) { 
		bzero(buff, MAX); 

		// read the message from client and copy it in buffer 
		read(sockfd, buff, sizeof(buff)); 
		// print buffer which contains the client contents 
		printf("From client: %s\t To client : ", buff); 
        if (strncmp("R", buff, 1)) {
			memmove (buff, buff+2, strlen (buff));

            num_samples = strtol(buff,&pEnd,10);
			uint16_t val = (uint16_t*)malloc(sizeof(uint16_t)*num_samples*ADCS);

            readADC(num_samples, &val);
			
			bzero(buff, MAX); 
			data_chunks = (ADCS*num_samples + (MAX / 2)) / MAX;

			// and send vals to client 
			for (size_t i = 0; i < data_chunks; i++)
			{
				memcpy(buff, val+i, MAX);
				write(sockfd, buff, MAX); 
			}
			
			free(val);

        }
		// if msg contains "Exit" then server exit and chat ended. 
		else if (strncmp("exit", buff, 4) == 0) { 
			printf("Server Exit...\n"); 
			break; 
		} 
		else
		{
			strcpy(buff, "Error: invalid request");
			write(sockfd, buff, sizeof(buff)); 
		}
		
	} 
} 

void streamData(int sockfd) { // Have to use threads
  	char buff[MAX]; 
    char * pEnd;
	int totSamples = MAX/ADCS;
	pthread_t thread; 

	while (1) { 
		bzero(buff, MAX); 

		// read the message from client and copy it in buffer 
		uint16_t *val = (uint16_t*)malloc(sizeof(uint16_t)*MAX);
		read(sockfd, buff, sizeof(buff)); 
		// print buffer which contains the client contents 
		printf("From client: %s\t To client : ", buff); 
        if (strncmp("S", buff, 1)) {
            // streamADC(); // source of segmentation error?
			pthread_create(&thread, NULL, streamADC, NULL);
			memmove (buff, buff+2, strlen (buff));

			// Need to use threads here


			
			bzero(buff, MAX); 
			

    		pthread_join(thread, NULL);
			// and send vals to client 
			
			memcpy(buff, streamVal, MAX);
			write(sockfd, buff, MAX); 
			

        }
		// if msg contains "Exit" then server exit and chat ended. 
		else if (strncmp("exit", buff, 4) == 0) { 
			printf("Server Exit...\n"); 
			break; 
		} 
		else
		{
			strcpy(buff, "Error: invalid request");
			write(sockfd, buff, sizeof(buff)); 
		}
		
	} 

}

// Driver function 
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

	// Function for chatting between client and server 
	sendData(connfd); 

	// After chatting close the socket 
	close(sockfd); 
} 
