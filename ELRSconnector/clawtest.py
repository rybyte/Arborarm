from gpiozero import PWMOutputDevice, Button, PWMLED
from time import sleep
import threading
import socket
import time
from signal import pause

# Define GPIO pins
SERVO_PIN = 13  # Servo connected to GPIO 6
#BUTTON_PIN = 13  # Button connected to GPIO 13

current_angle = 50

# Initialize PWM for the servo
servo = PWMOutputDevice(SERVO_PIN)  # Create a PWM output device for the servo
servo.value = 0  # Start with the servo at the 0 position

# Button setup
#button = Button(BUTTON_PIN, pull_up=True)  # Use internal pull-up resistor

# Servo control variables
servo1_open = True

# Function to move the servo
def set_servo_angle(angle):
    duty = 0.025 + (angle / 180) * 0.10  # Normalize angle to [0, 1] range
    servo.value = duty  # Set PWM duty cycle to control the servo position

# Function to handle button press
def toggle_servo():
    global servo1_open
    if servo1_open:
        set_servo_angle(140)  # Open position
    else:
        servo.on()  # Close position
    servo1_open = not servo1_open

# Attach the function to button press
#button.when_pressed = toggle_servo
def listen_socket():
    global current_angle
    HOST = 'localhost'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        while True:
            data = client_socket.recv(1024)
            if not data:
                print("Server disconnected.")
                break

            data_str = data.decode('utf-8').strip()
            try:
                channel_value = int(data_str)
                if channel_value < 1600 and channel_value > 100:
                    angle = 80
                elif channel_value > 1600 and channel_value < 1800:
                    angle = 140
                else:
                    angle = current_angle
                print(angle)
                if angle != None and abs(current_angle - angle) >= 5:
                    set_servo_angle(angle)
                    print(f"Received RC input: {channel_value}, Setting servo angle: {angle:.2f}")

            except ValueError:
                print(f"Invalid data received: {data_str}")

# Start socket listening in a separate thread
socket_thread = threading.Thread(target=listen_socket, daemon=True)
socket_thread.start()
print("Claw started")

print("Listening for socket commands...")
pause()  # Keeps script running
