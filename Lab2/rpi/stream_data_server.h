#include <stdio.h> 
#include <netdb.h> 
#include <netinet/in.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 


#define PORT 8080 
#define SA struct sockaddr 
#define HEADERSIZE 20


void sendData(int sockfd);

int main();

