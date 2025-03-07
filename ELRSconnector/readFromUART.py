#!/usr/bin/env python3
import serial
import time
import argparse
from enum import IntEnum
import socket
import time


CRSF_SYNC = 0xC8

class PacketsTypes(IntEnum):
    RC_CHANNELS_PACKED = 0x16

def crc8_dvb_s2(crc, a) -> int:
    crc = crc ^ a
    for ii in range(8):
        if crc & 0x80:
            crc = (crc << 1) ^ 0xD5
        else:
            crc = crc << 1
    return crc & 0xFF

def crc8_data(data) -> int:
    crc = 0
    for a in data:
        crc = crc8_dvb_s2(crc, a)
    return crc

def crsf_validate_frame(frame) -> bool:
    return crc8_data(frame[2:-1]) == frame[-1]

def extract_channel(data, channel_index):
    """Extracts the value of a specific channel from RC_CHANNELS_PACKED payload."""
    bit_position = channel_index * 11  # Starting bit position for the channel
    byte_index = bit_position // 8     # Starting byte index
    bit_offset = bit_position % 8      # Bit offset within the byte

    # Extract the channel value (11 bits)
    channel_value = (data[byte_index] >> bit_offset) | \
                    ((data[byte_index + 1] << (8 - bit_offset)) & 0x07FF)

    return channel_value

def handleCrsfPacket(ptype, data):
    try:
        if ptype == PacketsTypes.RC_CHANNELS_PACKED:
            # Extract channel 5 (index starts at 0)
            channel_5_value = extract_channel(data[3:], channel_index=6)
            print(f"Channel 5 Value: {channel_5_value}")
        else:
            pass
        return channel_5_value
    except:
        channel_5_value = "0"
        return channel_5_value


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-P', '--port', default='/dev/ttyAMA0', required=False)
parser.add_argument('-b', '--baud', default=420000, required=False)
parser.add_argument('-s', '--socket_port', default=65432, type=int, required=False)
args = parser.parse_args()

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', args.socket_port))
server_socket.listen(1)  # Allow one pending connection

print(f"Socket server listening on port {args.socket_port}...")

# Accept a client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

with serial.Serial(args.port, args.baud, timeout=2) as ser:
    input_buffer = bytearray()
    while True:
        if ser.in_waiting > 0:
            input_buffer.extend(ser.read(ser.in_waiting))
        else:
            time.sleep(0.020)

        while len(input_buffer) > 2:
            expected_len = input_buffer[1] + 2
            if expected_len > 64 or expected_len < 4:
                input_buffer = bytearray()
            elif len(input_buffer) >= expected_len:
                single_packet = input_buffer[:expected_len]
                input_buffer = input_buffer[expected_len:]

                if not crsf_validate_frame(single_packet):
                    print("CRC error")
                else:
                    channel_state = handleCrsfPacket(single_packet[2], single_packet)
                    print(f"Processing packet: {single_packet}")
                    
                    # Convert channel_state to a string if necessary
                    channel_state_str = str(channel_state)
                    
                    # Publish the channel_state via socket
                    try:
                        print(f"Sending channel_state to client: {channel_state_str}")
                        conn.sendall(channel_state_str.encode('utf-8'))  # Send data to the client
                        print("Channel_state sent successfully.")
                    except ConnectionResetError:
                        print("Client disconnected. Waiting for new connection...")
                        conn, addr = server_socket.accept()
                        print(f"New connection from {addr}")
                    except Exception as e:
                        print(f"Error sending channel_state: {e}")
            else:
                break

# Close the socket connection when done
conn.close()
server_socket.close()
