/**
 * @file weather.c
 * @author bhagwat shinde (bhagwat.shinde0799@gmail.com)
 * @brief  Application to collect sensor data from individual sensor file at /tmp location and create single csv file
 * @version 0.3 weather file restoring back to previous version for save in sd card with proper date time name
 * @date 2022-08-29
 * 
 * @copyright Copyright (c) 2022
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

// temperature and humidity sensor data file
#define MET_RAM_FILE_PATH "/tmp/met"

// light sensor data file
#define LIGHT_RAM_FILE_PATH "/tmp/light_intensity"

// gps data file path
#define GPS_FILE_PATH "/tmp/gps"

// configuration file containing device serial ID and other details
#define CONF_FILE_PATH "/etc/entomologist/ento.conf"

// file open mode
#define RAM_FILE_MODE "r"

//path to store final csv file
char file_path[] = "/media/mmcblk1p1/upload/";

//char file_path[] = "/tmp/";
char file_extension[] = ".csv";
char serial_ID[20];



time_t now;
struct tm ts;
char  time_buf[30];
char time_str[30];

char *csv_filename;

//initilizing all values
float temp_c = 0,temp_f = 0,humidity = 0,Lux = 0;
char latitude[20] = "NA",longitude[20]="NA",gps_state[20]="NA",gps_status[20]="NA",altitude[20]="NA",satellites[20]="NA",gps_time[20]="NA";

//funtion read serial id of device from /etc/entomologist/ento.conf file
void serial_id()
{
        char name[20];

        // this is format of configuration file ento.conf. If format of config file changes this function will fail causing code to exit. This can be implemented with cJSON library.
        const char * SERIAL_ID_FORMAT = "{\n    \"device\": {\n\t\"NAME\": \"%[^\"]\",\n\t\"SERIAL_ID\": \"%[^\"]\",}";

        FILE * file;
        char *filename = CONF_FILE_PATH;
        //char *filename = "ento.conf";
        file = fopen(filename, RAM_FILE_MODE);
        if(file == NULL)
        {       printf("can not open file %s\n",filename);
                exit(1);
        }

        // read data from file into given variables
        if(fscanf(file,SERIAL_ID_FORMAT, name, serial_ID) == EOF)
        {
                printf("Error reading file %s\n",filename);
                exit(1);
        }

}

//function to record current data and time
void date_time_fuc()
{
        time ( &now );
        ts = *localtime ( &now );

        // time format to save in csv file
        strftime(time_buf, sizeof(time_buf), "%a %Y-%m-%d %H:%M:%S %Z", &ts);

        // timestamp for file_name
        strftime(time_str, sizeof(time_str), "weather_%d-%m-%Y_%H_", &ts);
        
}

/*
this function crate unique filename which is must to upload file to cloud. file name start with weather_ the add date and hour,serialID of device and last .csv extension
example file is weather_29-08-2022_11_D0310.csv
*/
void filename_func()
{
        date_time_fuc();
        serial_id();

        csv_filename = malloc(strlen(time_str) + strlen(file_path) + strlen(file_extension) + 1);
        if(csv_filename == NULL)
        {
                printf("Error allocating memory for filename\n");
                exit(1);
        }
        csv_filename[0] = '\0';   // ensures the memory is an empty string
        strcat(csv_filename,file_path);
        strcat(csv_filename,time_str);
        strcat(csv_filename,serial_ID);
        strcat(csv_filename,file_extension);

}

/*
This function read /tmp/met file which contain temperature and humidity data
eg file format
{
    "Relative_humidity":"68.51", 
    "Temperature(C)":"23.57", 
    "Temperature(F)":"74.43"
}
*/
float read_met_data()
{
        //variable to store humidity,temperature in degree celcius and Fahrenheit
        char temp_data1[20];
        char temp_data2[20];
        char temp_data3[20];

        // /tmp/met file format
        const char * MET_FILE_FORMAT = "{\n\t\"Relative_humidity\":\"%[^\"]\",\n\t\"Temperature(C)\":\"%[^\"]\",\n\t\"Temperature(F)\":\"%[^\"]\"}";

        FILE * file;
        char *filename = MET_RAM_FILE_PATH;
        //char *filename = "met";
        file = fopen(filename,RAM_FILE_MODE);
        if(file == NULL)
        {       printf("can not open file %s\n",filename);
                //exit(1);
                return 1;
        }

        // scanning file data into variable
        if(fscanf(file,MET_FILE_FORMAT, temp_data1, temp_data2, temp_data3) == EOF)
        {
                printf("Error reading file %s\n",filename);
                //exit(1);
                return 1;
        }

        // converting final data to float
        humidity = atof(temp_data1);
        temp_c = atof(temp_data2);
        temp_f = atof(temp_data3);


}

/*
function read gps data from /tmp/gps file. Here we read all the parameters from file and only take required longitude and latitude data.
eg file format
{
      "time":"2022-08-29T12:12:49",
      "gps_state":"modem_not_found",
      "location":{
              "status":"",
              "latitude":"",
              "longitude":"",
              "altitude":"",
              "satellites":"00"
      }
}
*/
int read_gps_data()
{
        // gps file format
        const char * GPS_FILE_FORMAT = "{\n\t\"time\":\"%[^\"]\",\n\t\"gps_state\":\"%[^\"]\",\n\t\"location\":{\n\t\t\"status\":\"%[^\"]\",\n\t\t\"latitude\":\"%[^\"]\",\n\t\t\"longitude\":\"%[^\"]\",\n\t\t\"altitude\":\"%[^\"]\",\n\t\t\"satellites\":\"%[^\"]\"\n\t\t}\n}";

        FILE * file;
        //char *filename = "/etc/entomologist/ento.conf";
        char *filename = GPS_FILE_PATH;
        file = fopen(filename, "r");
        if(file == NULL)
        {       printf("can not open file %s\n",filename);
                return 1;
        }

        if(fscanf(file,GPS_FILE_FORMAT, gps_time, gps_state, gps_status,latitude,longitude,altitude,satellites) == EOF)
        {
                printf("Error reading file %s\n",filename);
                return 1;
        }


}

/*
funtion read light sensor data from /tmp/light_intensity file
eg file format
{
  "Light_intensity":"221.82"
}
*/
float read_light_data()
{
        //store light intensity data
        char temp_data1[20];

        //file format
        const char * LIGHT_FILE_FORMAT = "{\n\t\"Light_intensity\":\"%[^\"]\"}";

        FILE * file;
        char *filename = LIGHT_RAM_FILE_PATH;
        file = fopen(filename, "r");
        if(file == NULL)
        {       printf("can not open file %s\n",filename);
                //exit(1);
                return 1;
        }

        if(fscanf(file,LIGHT_FILE_FORMAT, temp_data1) == EOF)
        {
                printf("Error reading file %s\n",filename);
                //exit(1);
                return 1;
        }

        //converting lux value to float
        Lux = atof(temp_data1);

}

/*
function which write all collected data to csv file
*/

int data_write()
{
        FILE * fptr;
        while(1)
        {
                read_light_data();
                read_gps_data();
                read_met_data();

                // time data
                date_time_fuc();

                //changing dynamic filename to constant. single line file in ram without header
                fptr = fopen(csv_filename,"a");
                if(fptr == NULL)
                {
                        printf("ERROR opening the file %s\n",csv_filename);
                        exit(1);
                }

                //writing data to file pointed by fptr pointer
                fprintf(fptr,"%s, %.2f, %.2f, %.2f, %s, %s\n", time_buf, humidity, temp_c, Lux, latitude, longitude);

                fclose(fptr);


                sleep(60);
        }
        return 0;
}

                //check if file exists
int checkIfFileExists(const char * filename)
{
        FILE *file;


        if (file = fopen(filename, "r"))
        {
                // if file open successfully means file already exist.
                fclose(file);
                return 0;
        }

        return 1;
}

int main()
{
        filename_func();
       //function check if the output csv file already exist for present hour, if not it will create new file with present date and hour else append data to current file
        // funtion does not create new file every hour. New file created only if code restart and file don't exist
        if(checkIfFileExists(csv_filename))
        {
                // open file for read
                FILE * fptr = fopen(csv_filename,"w");
                if(fptr == NULL)
                {
                        printf("ERROR creating the file %s\n",csv_filename);
                        exit(1);
                }

                fprintf(fptr,"Date_time, Relative_Humidity(%%), Temperature(C), Light_intensity(Lux), Latitude, Longitude\n");

                fclose(fptr);

        }

        data_write();

        return 0;
}