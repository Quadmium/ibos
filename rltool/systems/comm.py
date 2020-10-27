import tkinter as tk
import pygubu
import socket
import sys
import time

class Application:
    
    def __init__(self):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('comm.ui')

        #3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow')

        builder.connect_callbacks(self)

        self.last_sent = None

        self.connect()
        
    def run(self):
        self.mainwindow.mainloop()

    def connect(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = ('localhost', 8080)
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)
        self.connection, client_address = sock.accept()

    def set_url_text(self, url):
        self.builder.get_variable("url_label_text").set("Current URL: {}".format(url))

    def on_button_send_click(self):
        if self.builder.get_variable("url_entry_text").get() == self.last_sent:
            return
        self.last_sent = self.builder.get_variable("url_entry_text").get()
        self.connection.sendall(self.last_sent.encode())
        self.set_url_text(self.connection.recv(1000).decode())


if __name__ == '__main__':
    app = Application()
    app.run()

'''
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
'''