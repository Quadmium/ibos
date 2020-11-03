import socket
import sys
import time
import struct

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8082)
sock.connect(server_address)
sock.sendall(struct.pack("!BBB", 5, 1, 0))

r = sock.recv(2)
print(r)

#state = connection.recv(1000).decode()

#print(state)