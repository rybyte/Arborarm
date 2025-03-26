#!/usr/bin/env bash

# Run Python scripts in the background and store their PIDs

python mergeUART.py & 
PID5=$!

sleep 5

python modTurningMotor.py & 
PID3=$!

sleep 1

python modTurningMotor_11.py & 
PID4=$!

sleep 1
python clawtest.py &
#python claw_copy.py & 
PID2=$!

sleep 0.5

./dual_cam.sh &
PID6=$!

# Function to handle cleanup
cleanup() {
    echo "Stopping all processes..."
    #kill $PID1 $PID2 $PID3 $PID4 2>/dev/null
    kill $PID5 $PID3 $PID4 $PID2 $PID6 2>/dev/null
    #kill $PID5 $PID3 $PID4 $PID2 2>/dev/null

    wait
    exit
}

# Trap SIGINT (Ctrl+C) and call cleanup function
trap cleanup SIGINT

# Wait indefinitely
while true; do sleep 1; done
