#ifndef VEML7700_H
#define VEML7700_H


#include <stdio.h>
#include "I2C.h"
#include <stdlib.h>


typedef unsigned short uint16_t;
typedef unsigned char uint8_t;

#define SLAVE_ADDR      0x10    // 7bit address last bit reserved for read/write
#define ALS_REG         0x04    // Lux value stored in this register

#define CONF_REG 0x00           // configuration register

#define RAM_FILE_PATH   "/tmp/light_intensity"

#define FILE_OPEN_MODE  "w"     //write mode - overwrite or create new file

// sensor configuration
int configure();

int read_light_intensity();


// write light intensity value to ram file
int write_to_file(float Lux, int mode);


#endif