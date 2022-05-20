#!/bin/bash

stamp() {
    TEXT=`jq '.device.SERIAL_ID' ento.conf` 
    DATE=`date +%d-%m-%Y` 
    TIME=`date +%H-%M-%S` 
    #ZONE=`date +"%Z %z"` 
    echo ${DATE}_${TIME}_${TEXT:1:-1}
}

while :
do
    var=`stamp`
    ffmpeg -f v4l2 -framerate 60 -video_size 1280x720 -i /dev/video0 -t 00:00:10 -q:v 2 -f MJPEG pipe:1 | ./ranacore -c ranacore.conf | ffmpeg -i - -q:v 2 -vcodec copy ${var}.avi
    sleep 5
done

#-frames 1000
#ffmpeg -f v4l2 -framerate 60 -video_size 1280x720 -i /dev/video0 -frames 1000 -q:v 1 -b 2000k -f MJPEG pipe:1 | ./ranacore64 -c ranacore.conf | ffmpeg -i - -q:v 1 -vcodec copy ranatest.avi

#ffmpeg -f v4l2 -framerate 60 -video_size 1280x720 -i /dev/video0 -frames 1000 -q:v 1 -b 2000k test.avi
