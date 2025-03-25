from gpiozero import Servo
from time import sleep
import threading
import socket
from signal import pause

from gpiozero.pins.pigpio import PiGPIOFactory

# Use pigpio for more accurate PWM
factory = PiGPIOFactory()

# Define GPIO pin (BCM numbering)
SERVO_PIN = 13  # GPIO13 (Pin 33)
servo = Servo(SERVO_PIN, pin_factory=factory, min_pulse_width=0.0005, max_pulse_width=0.0025)

# Track current servo angle
current_angle = 140

def angle_to_value(angle):
    """Convert angle (0 to 180) to gpiozero Servo value (-1 to 1)"""
    return max(-1.0, min(1.0, (angle - 90) / 90.0))  # Clamp between -1 and 1

def set_servo_angle(angle):
    global current_angle
    current_angle = angle
    servo_value = angle_to_value(angle)
    servo.value = servo_value
    sleep(0.1)

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
                if angle is not None and abs(current_angle - angle) >= 5:
                    set_servo_angle(angle)
                    print(f"Received RC input: {channel_value}, Setting servo angle: {angle:.2f}")

            except ValueError:
                print(f"Invalid data received: {data_str}")

# Start socket listener in a thread
socket_thread = threading.Thread(target=listen_socket, daemon=True)
socket_thread.start()

print("Starting Claw")
print("Listening for socket commands...")

pause()
