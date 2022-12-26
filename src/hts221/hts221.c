/*
        @author         Bhagwat Shinde
        name            hts221.c
        Description     Library for interfacing hts221 light and humidity sensor
        date            30 April 2022

        How to use      include hts221.h file in your mainn code and you are ready to use fuctions
        compilation     gcc main.c hts221.c I2C.c -o output

        Note            change the i2c_bus (i2c adapter as per your board)
*/
#include "hts221.h"
#include "I2C.h"



// calibration parameters

//fixed value - read only once

uint8_t H0;             //0x30
uint8_t H1;             //0x31

int16_t H2;             //0x36 & 0x37
int16_t H3;             //0x3a & 0x3b

uint16_t T0;            //0x32
uint16_t T1;            //0x33

uint16_t raw;            //0x35

int16_t T2;              //0x3c & 0x3d
int16_t T3;              //0x3e & 0x3f

// this two values get updated

int16_t hum;             //0x28 & 0x29
int16_t temp;            //0x2a & 0x2b


#define heater_on_time  10 // in seconds

const char * DATA_OUT_FORMAT = "{\n\t\"Relative_humidity\":\"%.2f\", \n\t\"Temperature(C)\":\"%.2f\", \n\t\"Temperature(F)\":\"%.2f\"\n}\n";


//configuring the sensor
int configure_sensor()
{
        uint8_t reg_addr = 0x10;
        uint8_t reg_value[1];
        reg_value[0] = 0x1b;
        uint8_t n_bytes = 1;
        uint8_t ret_value = i2c_write(SLAVE_ADDR, reg_addr,reg_value,n_bytes);
        if(ret_value == -1)
        {
                printf("configuring sensor failed\n");
                exit(1);
        }

        reg_addr = 0x20;
        reg_value[0] = 0x85;
        n_bytes = 1;
        ret_value = i2c_write(SLAVE_ADDR, reg_addr,reg_value,n_bytes);
        if(ret_value == -1)
        {
                printf("configuring sensor failed\n");
                exit(1);
        }

        return 0;
}


// read calibration data only once
int read_calibration_data()
{
        uint8_t reg_addr = 0x30;
        uint8_t reg_value[2]={0};
        uint8_t n_bytes = 1;
        uint8_t * p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);
        if(p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }


        H0 = *(p_ret_data);
        H0 = H0/2;

        reg_addr = 0x31;
        n_bytes = 1;

        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);
        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }

        H1 = *(p_ret_data);
        H1 = H1/2;



        reg_addr = 0x36 | 0x80;// | 0x80 auto increment reg value
        n_bytes = 2;
        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }
        
        H2 = (uint16_t)(*(p_ret_data+1)) << 8 | *p_ret_data ;


        reg_addr = 0x3a | 0x80;// | 0x80 auto increment reg value
        n_bytes = 2;
        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }
        
        H3 = (uint16_t)(*(p_ret_data+1)) << 8 | *p_ret_data ;



        reg_addr = 0x32;
        n_bytes = 1;
        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }
       
        T0 = *(p_ret_data);



        reg_addr = 0x33;
        n_bytes = 1;
        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }
        
        T1 = *(p_ret_data);

        reg_addr = 0x35;
        n_bytes = 1;
        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }
       
        raw = *(p_ret_data);

        // Convert the temperature Calibration values to 10-bits
        T0 = ((raw & 0x03) * 256) + T0;
        T1 = ((raw & 0x0C) * 64) + T1;



        reg_addr = 0x3c | 0x80;// | 0x80 auto increment reg value
        n_bytes = 2;
        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }

        T2 = (uint16_t)(*(p_ret_data+1)) << 8 | *p_ret_data ;


        reg_addr = 0x3e | 0x80;// | 0x80 auto increment reg value
        n_bytes = 2;
        p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("Read_calibration_data failed\n");
                exit(1);
        }

        T3 = (uint16_t)(*(p_ret_data+1)) << 8 | *p_ret_data ;


        return 0;        
}

//read temperature data
float read_temperature()
{
        uint8_t reg_addr = 0x2a | 0x80;// | 0x80 auto increment reg value
        uint8_t n_bytes = 2;
        uint8_t * p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("read temperature failed\n");
                exit(1);
        }

        temp = (uint16_t)(*(p_ret_data+1)) << 8 | *p_ret_data ;

        float cTemp = ((T1 - T0) / 8.0) * (temp - T2) / (T3 - T2) + (T0 / 8.0);
        //float fTemp = (cTemp * 1.8 ) + 32;
        return cTemp;

}

//read humidity value
float read_humidity()
{
        uint8_t reg_addr = 0x28 | 0x80;// | 0x80 auto increment reg value
        uint8_t n_bytes = 2;
        uint8_t * p_ret_data = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);

        if( p_ret_data == NULL)
        {
                printf("read humidity failed\n");
                exit(1);
        }


        hum = (uint16_t)(*(p_ret_data+1)) << 8 | *p_ret_data ;

        float humidity = ((1.0 * H1) - (1.0 * H0)) * (1.0 * hum - 1.0 * H2) / (1.0 * H3 - 1.0 * H2) + (1.0 * H0);
        return humidity;
}

// enable internal heater for humidity saturation
int EnableHeater()
{
        //Read 1 byte of data from address(0x21)
        uint8_t reg_addr = 0x21;
        uint8_t n_bytes = 1;
        uint8_t * p_ret_val = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);
        if( p_ret_val == NULL)
        {
                printf("Heater enabled failed\n");
                exit(1);
        }

        uint8_t reg_data[2];
        reg_data[0] = *p_ret_val | 0x02; 
        int ret_val = i2c_write(SLAVE_ADDR, reg_addr,reg_data, n_bytes);
        if(ret_val < 0 )
        {
                printf("Heater enabled failed\n");
                exit(1);
        }
        printf("Heater enabled.\n");
        return 0;

}

// Heater disable function
int DisableHeater()
{
        //Read 1 byte of data from address(0x21)
        uint8_t reg_addr = 0x21;
        uint8_t n_bytes = 1;
        uint8_t * p_ret_val = i2c_read(SLAVE_ADDR, reg_addr,n_bytes);
        if( p_ret_val == NULL)
        {
                printf("Heater disable failed\n");
                exit(1);
        }

        uint8_t reg_data[2];
        reg_data[0] = *p_ret_val & ~(0x02);
        i2c_write(SLAVE_ADDR, reg_addr,reg_data, n_bytes);
        int ret_val = i2c_write(SLAVE_ADDR, reg_addr,reg_data, n_bytes);
        if(ret_val < 0 )
        {
                printf("Heater disable failed\n");
                exit(1);
        }
        printf("Heater Disabled.\n");
        return 0;
}

int write_to_file(int mode)
{
        


        FILE *fptr;
        while(1)
        {
                // reading humidity value
                float humidity = read_humidity();

                // reading temperature data
                float cTemp = read_temperature();
                
                
                if(humidity > 95)
                {
                        humidity = read_humidity();
                }


                while(humidity > 98 && cTemp < 10)
                {
                        //enable heater
                        EnableHeater();

                        sleep(heater_on_time);

                        // disabling the heater
                        DisableHeater();

                        //waiting for reading to be normal after heater cycle
                        sleep(30);

                        humidity = read_humidity();
                        cTemp = read_temperature();


                }
                float fTemp = (cTemp * 1.8 ) + 32;


                 
                if(humidity < 2)
                {
                        humidity = 2;
                }

                if(humidity > 99)
                {
                        humidity = 99;
                }


                //opening the file
                fptr = fopen(RAM_FILE_PATH,MODE);
                if( fptr == NULL)
                {
                        printf("Can not open file %s\n",RAM_FILE_PATH);
                        exit(1);
                }

                if(fprintf(fptr,DATA_OUT_FORMAT, humidity, cTemp, fTemp)<0)
                {
                        printf("Error : write to file \n");
                        exit(1);
                }

                // //writing Relative humidity to file
                // if(fprintf(fptr,"Relative_Humidity:%.2f\n",humidity )<0)
                // {
                //         printf("error writing relative humidity to file \n");
                //         exit(1);     
                // }



                // //writing Temperature to file
                // if(fprintf(fptr,"Temperature(C):%.2f\n",cTemp )<0)
                // {
                //         printf("error writing temperature (C) to file \n");
                //         exit(1);     
                // }

                // //writing Temperature to file
                // if(fprintf(fptr,"Temperature(F):%.2f\n",fTemp )<0)
                // {
                //         printf("error writing temperature (F) to file \n");   
                //         exit(1);  
                // }


                if( fclose(fptr) == EOF)
                {
                        printf("Can not close file /tmp/ambient_data\n");
                        exit(1);
                }
                sleep(10);

                if (mode == 2){
                    exit(0);
                }
        }
        return 0;
}

