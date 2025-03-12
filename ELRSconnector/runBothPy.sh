#!/usr/bin/env bash

# Run Python scripts in the background and store their PIDs
#python readFromUART.py & 
#PID1=$!

#sleep 2

#python turningMotor.py & #
#PID2=$!

#sleep 2
python mergeUART.py & #
PID5=$!

sleep 2

python modTurningMotor.py & 
PID3=$!

sleep 2
#python readFromUART_11.py & 
#PID3=$!

#sleep 2

python modTurningMotor_11.py & 
PID4=$!

# Function to handle cleanup
cleanup() {
    echo "Stopping all processes..."
    #kill $PID1 $PID2 $PID3 $PID4 2>/dev/null
    kill $PID4 $PID3 $PID5 2>/dev/null

    wait
    exit
}

# Trap SIGINT (Ctrl+C) and call cleanup function
trap cleanup SIGINT

# Wait indefinitely
while true; do sleep 1; done
