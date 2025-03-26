from gpiozero import AngularServo
from time import sleep
import threading
import socket
from signal import pause

SERVO_PIN = 13  # BCM pin number
servo = AngularServo(
    SERVO_PIN,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

current_angle = 140

def set_servo_angle(angle):
    global current_angle
    if angle != current_angle:
        current_angle = angle
        servo.angle = angle
        print(f"Set servo angle to {angle}")
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
                if 100 < channel_value < 1600:
                    angle = 80
                elif 1600 < channel_value < 1800:
                    angle = 140
                else:
                    angle = current_angle

                if abs(current_angle - angle) >= 5:
                    set_servo_angle(angle)
                    print(f"RC input: {channel_value}, Servo angle: {angle}")
            except ValueError:
                print(f"Invalid data received: {data_str}")

# Start socket listener in background
socket_thread = threading.Thread(target=listen_socket, daemon=True)
socket_thread.start()

print("AngularServo (software PWM) initialized and listening...")
pause()
