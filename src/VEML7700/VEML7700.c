#include "VEML7700.h"

const char * DATA_OUT_FORMAT = "{\n\t\"Light_intensity\":\"%.2f\"\n}\n";

// configuring the sensor

int configure()
{
    //writing 0x0000 to the configuration register i.e 0x00 
    uint8_t reg_addr = CONF_REG;
    uint8_t reg_data[2];
    reg_data[0] = 0x00;
    reg_data[1] = 0x00;
    uint8_t n_bytes = 2;
    int ret_val = i2c_write(SLAVE_ADDR, reg_addr ,reg_data, n_bytes);
    if(ret_val == -1)
    {
        printf("Fail to configure light sensor \n");
        exit(1);
    }
}

int read_light_intensity()
{
    //Read ALS_REG
    uint8_t reg_addr = ALS_REG;
    uint8_t n_bytes = 2;
    uint8_t * p_ret_val = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);
    if(p_ret_val == NULL)
    {
        printf("Fail to read light intensity\n");
        exit(1);
    }
    //Combine higher byte and lower byte of register
    return ((uint16_t)(*(p_ret_val+1)) << 8 | *p_ret_val);
    
}


int write_to_file(float Lux, int mode)
{
    FILE *fptr;
    
    //opening the file
    fptr = fopen(RAM_FILE_PATH,FILE_OPEN_MODE);

    //check if file opened successfully
    if(fptr == NULL)
    {
            printf("Error opening the file /tmp/light_intensity");
            exit(1);
    }
    
    
    if(fprintf(fptr,DATA_OUT_FORMAT, Lux)<0)
    {
            printf("Error :  light intensity - write to file \n");
            exit(1);
    }


    // //writing light intensity to file
    // if(fprintf(fptr,"Light_Intensity:%0.2f\n",Lux )<0)
    // {   
    //         printf("error writing temperature to file \n");
    //         exit(1);     
    // }

    if(fclose(fptr) == EOF)
    {
        printf("Error closing file : /tmp/light_intensity");
        exit(1);
    }
    

    if (mode == 2){
        exit(0);
    }
    return 0;
}


