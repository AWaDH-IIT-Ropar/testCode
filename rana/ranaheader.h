/**************************************************************************
 * Rana header block which prefixes image data read and written by ranacore
 * (C) M.A. O'Neill, Tumbling Dice, 2022
 *************************************************************************/

#ifndef RANAHEADER_H
#define RANAHEADER_H

#include <stddef.h>
#include <time.h>


/*---------*/
/* Defines */
/*---------*/
/*---------------------*/
/* Rana header version */
/*---------------------*/

#define RANAHEADER_VERSION "1.00"


/*-------------------*/
/* Rana header magic */
/*-------------------*/

#define RANAHEADER_MAGIC_SIZE  18 
#define RANAHEADER_MAGIC       "ranaheader-V-1.00 "


/*-------------------------------*/
/* Maximum size of header string */
/*-------------------------------*/

#define RANAHEADER_STRING_SIZE  256


/*---------------------------*/
/* Stream multiplexor states */
/*---------------------------*/

#define MOTION     (1 << 0)
#define POSTCAP    (1 << 1)
#define TIMELAPSE  (1 << 3)


/*--------------------------*/
/* ranacore header/metadata */
/*--------------------------*/

typedef struct {

	            /*-------*/
                    /* Magic */
	            /*-------*/

	            unsigned char     magic[RANAHEADER_MAGIC_SIZE];


	            /*----------------*/
	            /* Size of header */
	            /*----------------*/

	            size_t            size;


		    /*-------------------*/
		    /* Frame name string */
		    /*-------------------*/

		    unsigned char      framename[RANAHEADER_STRING_SIZE]; 


		    /*-----------------*/
		    /* Blob parameters */
		    /*-----------------*/

		                                                       /*----------------------------*/
                    float              blob_cx;                        /* Centre of motion [x]       */
	            float              blob_cy;                        /* Centre of motion [y]       */
		    float              blob_xrad;                      /* Blob [x] radius            */
		    float              blob_yrad;                      /* Blob [y] radius            */
		    float              blob_diff_density;              /* Blob diff density          */
                    float              blobness;                       /* Blob diff-contrast         */
		                                                       /*----------------------------*/


		    /*------------*/
		    /* Time stamp */
		    /*------------*/
                                                                       /*-----------------------------*/
		    double             time_stamp;                     /* Time to nearest millisecond */
                                                                       /*-----------------------------*/


		    /*------------------------------------*/
		    /* Time stamp (human readable string) */
		    /*------------------------------------*/

		    unsigned char     datetime[RANAHEADER_STRING_SIZE];


		    /*-----------*/
		    /* Time zone */
		    /*-----------*/

		    unsigned char     tzone[RANAHEADER_STRING_SIZE];


		    /*------------------*/
		    /* Frame identifier */
		    /*------------------*/

		    unsigned long int  frame_id;


		    /*-------------------------*/
		    /* Event type and identify */
		    /*-------------------------*/
		    /*----------------------------------------------*/
		    /*  Cardinal number:  motion event identifier   */
		    /*  MOTION:    motion capture image frame event */
		    /*  POSTCAP:   post motion capture image frame  */
		    /*  TIMELAPSE: timelapse image frame            */
		    /*----------------------------------------------*/

		    unsigned int      event_id;
		    short int         event_type;


		    /*-----------------------------------------*/
		    /* Geodetic location (latitude, longitude) */
                    /* Assumes GPS board on logger hardware    */
		    /*-----------------------------------------*/

                    double            latitude;
		    double            longitude;


                    /*----------------------------------------------*/
                    /* Weather (assumes weather board with          */
                    /* BME299 and Sill32 sensors on logger hardware */
                    /*----------------------------------------------*/

                                                        /*-------------------------------*/
                    float               temperature;    /* Ambient temperature (Celsius) */
                    float               pressure;       /* Pressure (Pascals)            */
                    float               humidity;       /* Relative humidity (percent)   */
                    float               altitude;       /* Altitude (metres)             */
                    float               uv_index;       /* UV index                      */
                                                        /*-------------------------------*/

                } ranaheader_type;

#endif /* RANAHEADER_H */
