#include <stdio.h>
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

// config file path
#define CONF_FILE_PATH "/etc/entomologist/fan_control.conf"
int temp_h=75000,temp_l=70000;// fan control temperature upper and lower limit - value/1000 - degree celsius


// check if file already exist to avoid gpio export error
int checkIfFileExists(const char * filename)
{
    FILE *file;
    if (file = fopen(filename, "r"))
    {
        fclose(file);
        return 0;
    }

    return 1;
}


// export the gpio pin 412
int export_gpio()
{
        char * filename = "/sys/class/pwm/pwmchip3/pwm0";
       
        if(checkIfFileExists(filename))
        {
                printf("exporting");
                // Export the desired pin by writing to /sys/class/gpio/export
                int fd = open("/sys/class/pwm/pwmchip3/export", O_WRONLY);
                if (fd == -1) {
                        perror("Unable to open /sys/class/pwm/pwmchip3/export");
                        exit(1);
                }
                // To write byte to export pwm0 file
                if (write(fd, "0", 1) != 1) {
                        perror("Error writing to /sys/class/pwm/pwmchip3/export");
                        close(fd);
                        exit(1);
                }
                close(fd);

                // period
                fd = open("/sys/class/pwm/pwmchip3/pwm0/period", O_WRONLY);
                if (fd == -1) {
                        perror("Unable to open /sys/class/pwm/pwmchip3/pwm0/period");
                        exit(1);
                }

                if (write(fd, "1000000", 7) != 7) {
                        perror("Error writing to /sys/class/pwm/pwmchip3/pwm0/period");
                        close(fd);
                        exit(1);
                }
                close(fd);

                // duty cycle
                fd = open("/sys/class/pwm/pwmchip3/pwm0/duty_cycle", O_WRONLY);
                if (fd == -1) {
                        perror("Unable to open /sys/class/pwm/pwmchip3/pwm0/duty_cycle");
                        exit(1);
                }

                if (write(fd, "1000000", 7) != 7) {
                        perror("Error writing to /sys/class/pwm/pwmchip3/pwm0/duty_cycle");
                        close(fd);
                        exit(1);
                }
                close(fd);

        }
        return 0;
}

int unexport_gpio()
{
        char * filename = "/sys/class/pwm/pwmchip3/unexport";
       
       //if file exist unexport int
        if(checkIfFileExists(filename) == 0)
        {
                 // Unexport the pin by writing to /sys/class/gpio/unexport

                int fd = open("/sys/class/pwm/pwmchip3/unexport", O_WRONLY);
                if (fd == -1) {
                        perror("Unable to open /sys/class/pwm/pwmchip3/unexport");
                        exit(1);
                }

                if (write(fd, "1", 1) != 1) {
                        perror("Error writing to /sys/class/pwm/pwmchip3/unexport");
                        exit(1);;
                }

                close(fd);

        }
        return 0;
}


// set the direction of gpio 412
int set_gpio_direction()
{
    // Set the pin to be an output by writing "out" to /sys/class/gpio/gpio24/direction
    int fd = open("/sys/class/gpio/gpio412/direction", O_WRONLY);
    if (fd == -1) {
        perror("Unable to open /sys/class/gpio/gpio412/direction");
        unexport_gpio();
        exit(1);
    }

    if (write(fd, "out", 3) != 3) {
        perror("Error writing to /sys/class/gpio/gpio412/direction");
        unexport_gpio();
        exit(1);
    }

    close(fd);
    return 0;
}

int read_temp()
{
    char buf[20];
    int core_temp = 0;

    // read temperature of thermal zone 0
    //char * filepath = "0";
    char * filepath = "/sys/devices/virtual/thermal/thermal_zone0/temp";
    char * MODE = "r";
    FILE* fd = fopen(filepath, MODE);
    if(fd == NULL) {
        printf("Unable to open %s",filepath);
        return -1;
    }
    fgets(buf,10,fd);
    int temp = atoi(buf);
    if(core_temp < temp)
    {
            core_temp = temp;
    }
    fclose(fd);

    // read temperature of thermal zone 1
    //filepath = "1";
    filepath = "/sys/devices/virtual/thermal/thermal_zone1/temp";
    MODE = "r";
    fd = fopen(filepath, MODE);
    if(fd == NULL) {
        printf("Unable to open %s",filepath);
        return -1;
    }
    fgets(buf,10,fd);
    temp = atoi(buf);
    if(core_temp < temp)
    {
            core_temp = temp;
    }
    fclose(fd);



    // read temperature of thermal zone 2
    //filepath = "2";
    filepath = "/sys/devices/virtual/thermal/thermal_zone2/temp";
    MODE = "r";
    fd = fopen(filepath, MODE);
    if(fd == NULL) {
        printf("Unable to open %s",filepath);
        return -1;
    }
    fgets(buf,10,fd);
    temp = atoi(buf);
    if(core_temp < temp)
    {
            core_temp = temp;
    }
    fclose(fd);


    // read temperature of thermal zone 3
    //filepath = "3";
    filepath = "/sys/devices/virtual/thermal/thermal_zone3/temp";
    MODE = "r";
    fd = fopen(filepath, MODE);
    if(fd == NULL) {
        printf("Unable to open %s",filepath);
        return -1;
    }
    fgets(buf,10,fd);
    temp = atoi(buf);
    if(core_temp < temp)
    {
            core_temp = temp;
    }
    fclose(fd);


    // read temperature of thermal zone 4
    filepath = "/sys/devices/virtual/thermal/thermal_zone4/temp";
    MODE = "r";
    fd = fopen(filepath, MODE);
    if(fd == NULL) {
        printf("Unable to open %s",filepath);
        return -1;
    }
    fgets(buf,10,fd);
    temp = atoi(buf);
    if(core_temp < temp)
    {
            core_temp = temp;
    }
    fclose(fd);


// thermal zone0 has default value 70000 does not change
//     // read temperature of thermal zone 5
//     filepath = "/sys/devices/virtual/thermal/thermal_zone5/temp";
//     MODE = "r";
//     fd = fopen(filepath, MODE);
//     if(fd == NULL) {
//         printf("Unable to open %s",filepath);
//         return -1;
//     }
//     fgets(buf,10,fd);
//     temp = atoi(buf);
//     if(core_temp < temp)
//     {
//             core_temp = temp;
//     }
//     fclose(fd);

//    printf("read temp core_temp: %d\n",core_temp);
    return core_temp;
}

int fan_on()
{
        //printf("In fan on");
        // turn fan off
        int fd = open("/sys/class/pwm/pwmchip3/pwm0/enable", O_WRONLY);
        if (fd == -1)
        {
                perror("Unable to open /sys/class/pwm/pwmchip3/pwm0/enable");
                return -1;
        }
        if (write(fd, "1", 1) != 1) {
            perror("Error : turning on fan");
            close(fd);
            return -1;
        }
        printf("Fan turned on\n");
        close(fd);
        return 0;
}

int fan_off()
{
        //printf("In fan off");
        // turn fan off
        int fd = open("/sys/class/pwm/pwmchip3/pwm0/enable", O_WRONLY);
        if (fd == -1)
        {
                perror("Unable to open /sys/class/pwm/pwmchip3/pwm0/enable");
                return -1;
        }
        if (write(fd, "0", 1) != 1) {
            perror("Error : turning off fan");
            close(fd);
            return -1;
        }
        close(fd);
        return 0;
        //printf("Fan turned off\n");

}

int control_fan()
{
        while(1)
        {
                int core_temp = read_temp();

                //printf("In control fan core_temp: %d\n",core_temp);

                if(core_temp < temp_l)
                {
                        // turn fan off
                        printf("fan off\n");
                        fan_off();
                }
                if(core_temp > temp_h)
                {
                        //turn on fan
                        printf("fan on\n");
                        fan_on();
                }
                //printf("end of control fan \n");
                sleep(20);
        }
}

void read_conf_file()
{
       const char * CONF_FILE_FORMAT = "{\n\t\"Temperature(L)\":%d,\n\t\"Temperature(H)\":%d\n}";

        FILE * file;
        char *filename = CONF_FILE_PATH;
        //char *filename = "ento.conf";
        file = fopen(filename, "r");
        if(file == NULL)
        {       printf("can not open file %s\n",filename);
                exit(1);
        }

        if(fscanf(file,CONF_FILE_FORMAT, &temp_l, &temp_h) == EOF)
        {
                printf("Error reading file %s\n",filename);
                exit(1);
        }
}

int main()
{
        //reading config file
        read_conf_file();

        export_gpio();
        
        //printf("gpio exported successfully\n");

        // set_gpio_direction();
        
        //printf("gpio direction set to output\n");

        //turn off fan
        fan_off();
        //printf("fan turned off manually\n");


        if(control_fan() == -1)
        {
                return -1;
        }
        //printf("after control fan\n");

        unexport_gpio();
       
        //printf("gpio unexported \n");
        return 0;
}