import tkinter as tk
import pygubu
import socket
import sys
import time

class Application(pygubu.TkApplication):
    def _create_ui(self):
        self.set_title("IBOS Comm")

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('comm.ui')

        #3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow')

        builder.connect_callbacks(self)

        self.connect()

    def run(self):
        self.update_loop()
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

    
    def update_loop(self):
        self.fetch_state()
        self.mainwindow.after(1000, self.update_loop)

    def fetch_state(self):
        self.connection.sendall(("FETCH-STATE#").encode())
        # TODO: add # delimiter at end of msg
        state = self.connection.recv(1000).decode().split("|")
        self.set_url_text(state[0])
        self.set_active_app_text(state[1])
        self.set_weblabels_text("Web Labels: \n{}\n\nNet Labels: \n{}".format(state[2], state[3]))
        self.builder.get_object("app_combobox").config(values=[x.split(" ")[1][:-1] for x in state[2].split("\n")])
        self.builder.get_object("app_combobox").bind('<<ComboboxSelected>>', self.on_app_combobox_select)
        self.builder.get_variable("app_combobox_text").set(state[1])

    def set_url_text(self, url):
        self.builder.get_variable("url_label_text").set("Current URL: {}".format(url))

    def set_active_app_text(self, text):
        self.builder.get_variable("active_app_text").set("Active Webapp: {}".format(text))
    
    def set_weblabels_text(self, text):
        self.builder.get_variable("weblabels_text").set(text)

    def on_button_send_click(self):
        new_url = self.builder.get_variable("url_entry_text").get()
        try:
            ip = socket.gethostbyname(new_url)
            self.connection.sendall(("MSG-NEW-URL|" + new_url + "|" + ip + "#").encode())
            self.fetch_state()
        except Exception as e:
            # TODO: WHAT DO WE DO IF THE DNS LOOKUP FAILS? prob send it to maude
            print("Exception: {}".format(e))

    def on_app_combobox_select(self, event):
        new_tab = self.builder.get_object("app_combobox").get()
        self.connection.sendall(("MSG-SWITCH-TAB|" + new_tab + "#").encode())
        self.fetch_state()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.run()
