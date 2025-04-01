#!/usr/bin/env python3
import serial
import time
import argparse
from enum import IntEnum
import socket

CRSF_SYNC = 0xC8

class PacketsTypes(IntEnum):
    RC_CHANNELS_PACKED = 0x16

def crc8_dvb_s2(crc, a) -> int:
    crc = crc ^ a
    for _ in range(8):
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
            channel_6_value = extract_channel(data[3:], channel_index=5)
            channel_7_value = extract_channel(data[3:], channel_index=6)
            #channel_10_value = extract_channel(data[3:], channel_index=9)
            channel_11_value = extract_channel(data[3:], channel_index=10)
        else:
            pass
        return str(channel_6_value), str(channel_7_value), str(channel_11_value)
    except:
        return "0", "0", "0"


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-P', '--port', default='/dev/ttyAMA0', required=False)
parser.add_argument('-b', '--baud', default=420000, required=False)
parser.add_argument('--socket_port_6', default=65431, type=int, required=False)
parser.add_argument('--socket_port_7', default=65432, type=int, required=False)
#parser.add_argument('--socket_port_10', default=65434, type=int, required=False)
parser.add_argument('--socket_port_11', default=65433, type=int, required=False)
args = parser.parse_args()

# Create two sockets (one for each channel)
server_socket_6 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_6.bind(('localhost', args.socket_port_6))
server_socket_6.listen(1)  

server_socket_7 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_7.bind(('localhost', args.socket_port_7))
server_socket_7.listen(1)  

#server_socket_10 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket_10.bind(('localhost', args.socket_port_10))
#server_socket_10.listen(1)

server_socket_11 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_11.bind(('localhost', args.socket_port_11))
server_socket_11.listen(1)

print(f"Socket server listening on port {args.socket_port_6} for Channel 6...")
print(f"Socket server listening on port {args.socket_port_7} for Channel 7...")
#print(f"Socket server listening on port {args.socket_port_10} for Channel 10...")
print(f"Socket server listening on port {args.socket_port_11} for Channel 11...")

# Accept client connections
conn_6, addr_6 = server_socket_6.accept()
print(f"Connected to Channel 6 client {addr_6}")

conn_7, addr_7 = server_socket_7.accept()
print(f"Connected to Channel 7 client {addr_7}")

#conn_10, addr_10 = server_socket_10.accept()
#print(f"Connected to Channel 10 client {addr_10}")

conn_11, addr_11 = server_socket_11.accept()
print(f"Connected to Channel 11 client {addr_11}")

with serial.Serial(args.port, args.baud, timeout=2) as ser:
    input_buffer = bytearray()
    while True:
        #time.sleep(2)
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
                    channel_6_state, channel_7_state, channel_11_state = handleCrsfPacket(single_packet[2], single_packet)
                    channel_6_state_str = str(channel_6_state)
                    channel_7_state_str = str(channel_7_state)
                    #channel_10_state_str = str(channel_10_state)
                    channel_11_state_str = str(channel_11_state)
                    # Send data to the respective socket clients
                    try:
                        conn_6.sendall(channel_6_state_str.encode('utf-8'))
                    except (ConnectionResetError, BrokenPipeError):
                        print("Channel 6 client disconnected. Waiting for new connection...")
                        conn_6, addr_6 = server_socket_6.accept()
                        print(f"New connection from {addr_6}")

                    try:
                        conn_7.sendall(channel_7_state_str.encode('utf-8'))
                    except (ConnectionResetError, BrokenPipeError):
                        print("Channel 7 client disconnected. Waiting for new connection...")
                        conn_7, addr_7 = server_socket_7.accept()
                        print(f"New connection from {addr_7}")

                    #try:
                        #conn_10.sendall(channel_10_state_str.encode('utf-8'))
                    #except (ConnectionResetError, BrokenPipeError):
                        #print("Channel 10 client disconnected. Waiting for new connection...")
                        #conn_10, addr_10 = server_socket_10.accept()
                        #print(f"New connection from {addr_10}")

                    try:
                        conn_11.sendall(channel_11_state_str.encode('utf-8'))
                    except (ConnectionResetError, BrokenPipeError):
                        print("Channel 11 client disconnected. Waiting for new connection...")
                        conn_11, addr_11 = server_socket_11.accept()
                        print(f"New connection from {addr_11}")

            else:
                break

# Close connections when done
conn_6.close()
conn_7.close()
#conn_10.close()
conn_11.close()
server_socket_6.close()
server_socket_7.close()
#server_socket_10.close()
server_socket_11.close()
