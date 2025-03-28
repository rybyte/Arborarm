#!/bin/bash

# Install FFmpeg and libcamera-tools if not already installed
echo "Checking for FFmpeg and libcamera..."
sudo apt update
sudo apt install ffmpeg libcamera-apps -y

# Identify USB Camera
USB_CAM="/dev/video0"

# Check if USB camera exists
if [ ! -e "$USB_CAM" ]; then
    echo "Error: USB webcam not found at $USB_CAM!"
    exit 1
fi

# Define Streaming Parameters
PC_IP="239.255.1.1"
USB_PORT="1234"
RPICAM_PORT="1235"
RESOLUTION="640x480"
FRAMERATE="30"
FIFO="/tmp/rpicam_fifo.h264"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Kill previous instances and clean up FIFO
pkill libcamera-vid
pkill ffmpeg
rm -f $FIFO
mkfifo $FIFO

# Start USB Camera Stream
echo "Starting USB Webcam Stream on udp://$PC_IP:$USB_PORT..."
ffmpeg -f v4l2 -framerate $FRAMERATE -video_size $RESOLUTION -i $USB_CAM \
-vf "drawtext=fontfile=$FONT: text='%{localtime}': fontcolor=white: fontsize=15: x=w-tw-10: y=h-th-10, \
     drawtext=fontfile=$FONT: text='USB Camera': fontcolor=yellow: fontsize=15: x=10: y=h-30" \
-f mpegts udp://$PC_IP:$USB_PORT &

# Start RPi Camera (v1.3) Stream into FIFO
echo "Starting RPi Camera 1.3 stream to FIFO..."
libcamera-vid -t 0 --inline --width 640 --height 480 --framerate $FRAMERATE -o $FIFO &

# Stream from FIFO using FFmpeg
echo "Starting RPi Camera Stream on udp://$PC_IP:$RPICAM_PORT..."
ffmpeg -f h264 -i $FIFO \
-vf "drawtext=fontfile=$FONT: text='%{localtime}': fontcolor=white: fontsize=20: x=w-tw-10: y=h-th-10, \
     drawtext=fontfile=$FONT: text='RPi Camera': fontcolor=yellow: fontsize=20: x=10: y=h-30" \
-f mpegts udp://$PC_IP:$RPICAM_PORT &

# Display Instructions
echo "Both cameras are now streaming with timestamps!"
echo "To view the streams on your PC using VLC:"
echo "  USB Webcam: udp://@${PC_IP}:${USB_PORT}"
echo "  RPi Camera: udp://@${PC_IP}:${RPICAM_PORT}"

# Keep script running
wait
