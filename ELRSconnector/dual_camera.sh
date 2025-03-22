#!/bin/bash

# Install FFmpeg if not already installed
echo "Checking for FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg not found, installing..."
    sudo apt update && sudo apt install ffmpeg -y
else
    echo "FFmpeg is already installed."
fi

# Identify Camera Devices
USB_CAM="/dev/video0"
ARDU_CAM="/dev/video1"

# Check if cameras exist
if [ ! -e "$USB_CAM" ]; then
    echo "Error: USB webcam not found at $USB_CAM!"
    exit 1
fi

if [ ! -e "$ARDU_CAM" ]; then
    echo "Error: ArduCam not found at $ARDU_CAM!"
    exit 1
fi

# Define Streaming Parameters
PC_IP="239.255.1.1"  # Mulitcast IP (type in udp://@<PC_IP>:<port_no.> on VLC to stream video)
USB_PORT="1234"       # USB Camera UDP Port
ARDU_PORT="1235"      # ArduCam UDP Port
RESOLUTION="640x480"
FRAMERATE="30"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Change font path if needed

# Start USB Camera Stream with Text Overlay
echo "Starting USB Webcam Stream on udp://$PC_IP:$USB_PORT..."
ffmpeg -f v4l2 -framerate $FRAMERATE -video_size $RESOLUTION -i $USB_CAM \
-vf "drawtext=fontfile=$FONT: text='%{localtime}': fontcolor=white: fontsize=15: x=w-tw-10: y=h-th-10, \
     drawtext=fontfile=$FONT: text='ARM Camera': fontcolor=yellow: fontsize=15: x=10: y=h-30" \
-f mpegts udp://$PC_IP:$USB_PORT &

# Start ArduCam Stream with Text Overlay
echo "Starting ArduCam Stream on udp://$PC_IP:$ARDU_PORT..."
ffmpeg -f v4l2 -framerate $FRAMERATE -video_size $RESOLUTION -i $ARDU_CAM \
-vf "drawtext=fontfile=$FONT: text='%{localtime}': fontcolor=white: fontsize=20: x=w-tw-10: y=h-th-10, \
     drawtext=fontfile=$FONT: text='ARM Camera': fontcolor=yellow: fontsize=20: x=10: y=h-30" \
-f mpegts udp://$PC_IP:$ARDU_PORT &

# Display Instructions
echo "Both cameras are now streaming with timestamps!"
echo "To view the streams on your PC using VLC:"
echo "  USB Webcam: udp://@239.225.1.1:1234"
echo "  ArduCam: udp://@239.225.1.1:1235"

# Keep script running
wait



