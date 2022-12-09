#include <stdio.h>
#include "VEML7700.h"


const char *i2c_bus = "/dev/apalis-i2c1";

int main(int argc, char *argv[])
{
	//i2c initialize
	i2c_init(i2c_bus);

	//configure the sensor
	configure();
	

	// gain = 1 and integration time = 100ms multiplication factor = 0.0576

	while(1)
	{
		// read light intensity
		int ret_val = read_light_intensity();

		float Lux = (float)ret_val * 0.0576;

		//write Lux value to ram file
		ret_val = write_to_file(Lux, argc);
		
		sleep(10);
	}

	
    
	// close the i2c bus
	i2c_close(i2c_bus);

	return 0;
}
