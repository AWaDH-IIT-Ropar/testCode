
#include "i2c_custom.h"


char *i2c_bus = "/dev/apalis-i2c1";
unsigned char slave_address = 0x09;
unsigned char reg;
unsigned char data_to_write[2];
unsigned char *data_to_read;


void ManufacturingID()
{
        reg = 0xFE;
        data_to_read = i2c_read(slave_address, reg);//reading result register
        printf("Manufacturing ID %02x",*(data_to_read+1));
        printf("%02x\n",*data_to_read);

}

void DeviceID()
{
        reg = 0xFF;
        data_to_read = i2c_read(slave_address, reg);//reading result register
        printf("Device ID %02x",*(data_to_read+1));
        printf("%02x\n",*data_to_read);
}


int main()
{
        i2c_init(i2c_bus);

        ManufacturingID();
        DeviceID();

        reg = 0x14;
        data_to_write[0] = 0x00;//lsb
        data_to_write[1] = 0x04;//msb
        i2c_write(slave_address, reg,data_to_write);//writing configuration register

        reg=0x15;
        data_to_write[0]= 0x00;//lsb
        data_to_write[1] = 0x38;//msb
        i2c_write(slave_address, reg,data_to_write);//writing configuration register


        
        

        

    
    i2c_close();
    return 0;
}
