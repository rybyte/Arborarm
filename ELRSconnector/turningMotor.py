import socket
import threading
from gpiozero import RotaryEncoder, Motor, PWMOutputDevice, Button
from signal import pause

# User Rotary Encoder (Direction Input)
user_encoder = RotaryEncoder(6, 5, wrap=True)

# Motor Setup
motor = Motor(forward=17, backward=18)  # Change pins as needed
pwm = PWMOutputDevice(13)  # Change to the correct PWM pin

# Stop Button (GPIO 26)
stop_button = Button(26)

def move_forward():
    """Starts moving forward immediately, stopping any previous movement."""
    print("Rotary Encoder moved FORWARD: Moving Motor Forward...")
    # stop_motor()  # Stop before switching direction
    pwm.value = 1  # Set speed to max (1 = full speed, 0 = stop)
    motor.forward()

def move_backward():
    """Starts moving backward immediately, stopping any previous movement."""
    print("Rotary Encoder moved BACKWARD: Moving Motor Backward...")
    # stop_motor()  # Stop before switching direction
    pwm.value = 1  # Set speed to max (1 = full speed, 0 = stop)
    motor.backward()

def stop_motor():
    """Stops the motor immediately."""
    print("Stopping Motor.")
    motor.stop()
    pwm.value = 0

# Detecting Rotary Encoder Movement
user_encoder.when_rotated_clockwise = move_forward
user_encoder.when_rotated_counter_clockwise = move_backward

# Stop motor when button is pressed
stop_button.when_pressed = stop_motor

def listen_socket():
    HOST = 'localhost'  # Hostname or IP address
    PORT = 65432        # Port number

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        while True:
            data = client_socket.recv(1024)  # Receive data from the server
            if data:
                print(f"Received: {data}")
                # Handle received data (e.g., trigger motor actions)
                if data == b"191":
                    move_forward()
                elif data == b"1792":
                    move_backward()
                elif data == b"1004":
                    stop_motor()
            else:
                print("No data received. Server disconnected.")
                break

# Start socket listening in a separate thread
socket_thread = threading.Thread(target=listen_socket)
socket_thread.daemon = True  # Allow the main thread to exit even if this thread is still running
socket_thread.start()

print("Rotary Encoder Motor Control is Running. Turn the encoder to move, or press the button to stop.")
pause()  # Keeps script running
