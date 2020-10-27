import socket
import sys
import time

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('localhost', 8080)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    connection, client_address = sock.accept()

    i = 0
    while True:
        connection.sendall("url{}".format(i).encode())
        i += 1
        print(connection.recv(1000).decode())
        time.sleep(5)

    connection.close()

if __name__ == '__main__':
    main()