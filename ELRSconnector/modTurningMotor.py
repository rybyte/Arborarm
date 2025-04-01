import socket
import threading
from gpiozero import Motor, PWMOutputDevice
from signal import pause
import time
# Motor Setup
motor = Motor(forward=17, backward=18)
pwm = PWMOutputDevice(27)

current = None  # Tracks last received data to avoid redundant actions

def move_forward():
    """Starts moving forward."""
    print("Moving Forward...")
    pwm.value = 0.5
    motor.forward()


def move_backward():
    """Starts moving backward."""
    print("Moving Backward...")
    pwm.value = 0.5
    motor.backward()

def stop_motor():
    """Stops the motor."""
    print("Stopping Motor.")
    motor.stop()
    pwm.value = 0

def listen_socket():
    global current
    HOST = 'localhost'
    PORT = 65431

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        while True:
            #time.sleep(2)
            data = client_socket.recv(1024)  # Receive data from the server
            if not data:
                print("Server disconnected.")
                break  # Exit loop if server disconnects

            # Clean and decode received data
            data_str = data.decode('utf-8').strip()

            # Process only if data changes
            current = data_str  # Update state tracking
            #print(f"Left Received: {data_str}")

            # Handle motor control
            if data_str == "191":
                move_forward()
            elif data_str == "256":
                move_backward()
            elif data_str == "485":
                stop_motor()
            else:
                print(f"Unknown command: {data_str}")

# Start socket listening in a separate thread
socket_thread = threading.Thread(target=listen_socket, daemon=True)
socket_thread.start()

print("Listening for socket commands...")
pause()  # Keeps script running
