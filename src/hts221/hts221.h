#ifndef HTS221_H
#define HTS221_H

#include <stdio.h> // printf()
#include <stdlib.h>
#include <sys/types.h> // open()
#include <sys/stat.h> // open()
#include <fcntl.h> // open()
#include <sys/ioctl.h> // ioctl()
#include <errno.h> // errno
#include <string.h> // strerror()
#include <unistd.h> // close()
#include <linux/i2c-dev.h> // struct i2c_msg
#include <linux/i2c.h> // struct i2c_rdwr_ioctl_data

#define SLAVE_ADDR 0x5f

typedef unsigned char uint8_t;
typedef unsigned short uint16_t;

#define RAM_FILE_PATH "/tmp/met"
#define MODE "w"

int configure_sensor();
int read_calibration_data();
float read_temperature();
float read_humidity();
int EnableHeater();
int DisableHeater();
int write_to_file();


#endif