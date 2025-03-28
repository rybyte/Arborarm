#!/bin/bash

# ─────────────────────────────
# RPi 5 Dual-Camera UDP Streamer
# USB camera + Pi Cam v1.3 over libcamera
# Stream both to VLC using multicast over UDP
# ─────────────────────────────

# Install FFmpeg and libcamera tools if missing
echo "Checking for FFmpeg and libcamera..."
sudo apt update
sudo apt install -y ffmpeg libcamera-apps

# Devices
USB_CAM="/dev/video0"
FIFO="/tmp/rpicam_fifo.h264"

# Multicast IP for VLC
PC_IP="239.255.1.1"
USB_PORT="1234"
RPICAM_PORT="1235"

# Settings
RESOLUTION="640x480"
FRAMERATE="30"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Clean up previous runs
echo "Cleaning up old processes and FIFOs..."
pkill libcamera-vid
pkill ffmpeg
rm -f $FIFO
mkfifo $FIFO

# ───── USB Camera ─────
if [ -e "$USB_CAM" ]; then
  echo "Starting USB Camera Stream on udp://@$PC_IP:$USB_PORT..."
  ffmpeg -f v4l2 -framerate $FRAMERATE -video_size $RESOLUTION -i $USB_CAM \
  -vf "drawtext=fontfile=$FONT: text='%{localtime}': fontcolor=white: fontsize=15: x=w-tw-10: y=h-th-10, \
       drawtext=fontfile=$FONT: text='USB Camera': fontcolor=yellow: fontsize=15: x=10: y=h-30" \
  -f mpegts udp://@$PC_IP:$USB_PORT &
else
  echo "Warning: USB camera not found at $USB_CAM"
fi

# ───── RPi Camera v1.3 via libcamera ─────
echo "Starting RPi Camera 1.3 stream to FIFO..."
libcamera-vid -t 0 --inline --nopreview --width 640 --height 480 --framerate $FRAMERATE -o $FIFO &

echo "Streaming RPi Camera from FIFO to udp://@$PC_IP:$RPICAM_PORT..."
ffmpeg -f h264 -i $FIFO \
-vf "drawtext=fontfile=$FONT: text='%{localtime}': fontcolor=white: fontsize=20: x=w-tw-10: y=h-th-10, \
     drawtext=fontfile=$FONT: text='RPi Camera': fontcolor=yellow: fontsize=20: x=10: y=h-30" \
-f mpegts udp://@$PC_IP:$RPICAM_PORT &

# ───── VLC Instructions ─────
echo ""
echo "🎥 Both cameras are now streaming over UDP!"
echo "📺 Open the following in VLC (Media > Open Network Stream):"
echo "  • USB Camera:  udp://@${PC_IP}:${USB_PORT}"
echo "  • RPi Camera:  udp://@${PC_IP}:${RPICAM_PORT}"
echo ""

# Keep script alive
wait
