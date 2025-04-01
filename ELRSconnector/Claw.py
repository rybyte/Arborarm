import RPi.GPIO as GPIO
from time import sleep
import threading
import socket
from signal import pause

# Define GPIO pins
SERVO_PIN = 13  # Servo connected to GPIO 13

# Setup GPIO
GPIO.setmode(GPIO.BCM)  
GPIO.setup(SERVO_PIN, GPIO.OUT)  

# Initialize PWM for the servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM for the servo
pwm.start(7.5)  # Set to middle position

current_angle = 140  # Track the last servo angle to avoid unnecessary updates

# Function to smoothly move the servo
def set_servo_angle(angle):
    global current_angle
    current_angle = angle
    duty = (angle / 18) + 2  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty)
    sleep(0.1)  # Allow time for movement

# Function to listen to socket
def listen_socket():
    global current_angle
    HOST = 'localhost'
    PORT = 65431

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

print("Starting Claw")
print("Listening for socket commands...")

pause()  # Keeps script running
