/*
adc_sampler.c
Public Domain
January 2018, Kristoffer KjÃ¦rnes & Asgeir BjÃ¸rgan
Based on example code from the pigpio library by Joan @ raspi forum and github
https://github.com/joan2937 | http://abyz.me.uk/rpi/pigpio/

Compile with:
gcc -Wall -lpthread -o adc_sampler adc_sampler.c -lpigpio -lm

Run with:
sudo ./adc_sampler

This code bit bangs SPI on several devices using DMA.

Using DMA to bit bang allows for two advantages
1) the time of the SPI transaction can be guaranteed to within a
   microsecond or so.

2) multiple devices of the same type can be read or written
   simultaneously.

This code reads several MCP3201 ADCs in parallel, and writes the data to a binary file.
Each MCP3201 shares the SPI clock and slave select lines but has
a unique MISO line. The MOSI line is not in use, since the MCP3201 is single
channel ADC without need for any input to initiate sampling.
*/
#include <pigpio.h>

/////// USER SHOULD MAKE SURE THESE DEFINES CORRESPOND TO THEIR SETUP ///////
#define ADCS 5      // Number of connected MCP3201.

#define OUTPUT_DATA "/home/pi/adcData.bin" // path and filename to dump buffered ADC data

/* RPi PIN ASSIGNMENTS */
#define MISO1 12     // ADC 1 MISO (BCM 4 aka GPIO 4).
#define MISO2 25     //     2
#define MISO3 18     //     3
#define MISO4 21    //     4
#define MISO5 16    //     5

#define MOSI 10     // GPIO for SPI MOSI (BCM 10 aka GPIO 10 aka SPI_MOSI). MOSI not in use here due to single ch. ADCs, but must be defined anyway.
#define SPI_SS 8    // GPIO for slave select (BCM 8 aka GPIO 8 aka SPI_CE0).
#define CLK 11      // GPIO for SPI clock (BCM 11 aka GPIO 11 aka SPI_CLK).
/* END RPi PIN ASSIGNMENTS */

#define BITS 12            // Bits per sample.
#define BX 4               // Bit position of data bit B11. (3 first are t_sample + null bit)
#define B0 (BX + BITS - 1) // Bit position of data bit B0.

#define NUM_SAMPLES_IN_BUFFER 300 // Generally make this buffer as large as possible in order to cope with reschedule.

#define REPEAT_MICROS 32 // Reading every x microseconds. Must be no less than 2xB0 defined above

#define DEFAULT_NUM_SAMPLES 31250 // Default number of samples for printing in the example. Should give 1sec of data at Tp=32us.
#define NUM_STREAM_SAMPLES 30
#define MAX  (ADCS*NUM_STREAM_SAMPLES*2)   // Number of bytes being sent at once. 



void getReading(int adcs, int *MISO, int OOL, int bytes, int bits, char *buf);

void recordSamples(rawWaveInfo_t rwi, int wid, int num_samples, uint16_t *val);

rawWaveInfo_t initADC();

void readADC(rawWaveInfo_t rwi, int wid, int sockfd, int done, char* buff);



