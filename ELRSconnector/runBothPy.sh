#!/usr/bin/env bash
#!/bin/bash

# Run the first Python script in the background
python readFromUART.py &
PID1=$!

# Wait for 2 seconds
sleep 2

# Run the second Python script in the background
python turningMotor.py &
PID2=$!

# Trap SIGINT to kill both processes
trap 'kill $PID1 $PID2; exit' SIGINT

# Wait indefinitely
while true; do sleep 1; done


