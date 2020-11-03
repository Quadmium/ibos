import tkinter as tk
import pygubu
import socket
import sys
import time
import subprocess as sp
import winlaunch
import atexit
import os

class BrowserContainer():
    def __init__(self, id, url, port):
        self.id = id
        self.url = url
        self.port = port

        self.start_browser()

    def start_browser(self):
        print("{} to port {}".format(self.url, self.port))
        self.browser_wid, self.browser_pid, self.browser_proc = winlaunch.launch("SOCKS5_SERVER=127.0.0.1:{} socksify firefox --new-instance {} -P {}".format(self.port, self.url, self.id))

    def show(self):
        winlaunch.win_activate(self.browser_wid)

    def hide(self):
        winlaunch.win_minimize(self.browser_wid)

    def kill(self):
        try:
            self.browser_proc.kill()
        except:
            pass

class Application(pygubu.TkApplication):
    def _create_ui(self):
        self.set_title("IBOS Comm")

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('comm_browser.ui')

        #3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow')

        builder.connect_callbacks(self)

        self.hijack = False

        self.tabs = {}

        self.cur_tab = -100

        self.open_webapps = {}
        self.last_webapp = 0

        self.connect()

    def on_exit(self):
        for tid in self.tabs:
            self.tabs[tid].kill()

    def run(self):
        self.update_loop()
        self.hijack_loop()
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

    def hijack_loop(self):
        if self.hijack and self.cur_tab != -1:
            x, y = winlaunch.win_pos(self.ibos_wid)
            s_x, s_y = winlaunch.win_size(self.ibos_wid)
            o_y = 10
            wid = self.tabs[self.cur_tab].browser_wid
            winlaunch.win_pos(wid, x-5, y+o_y)
            winlaunch.win_size(wid, s_x - 13, 600)
        self.mainwindow.after(1, self.hijack_loop)

    def fetch_state(self):
        self.connection.sendall(("FETCH-STATE#").encode())
        # TODO: add # delimiter at end of msg
        state = self.connection.recv(1000).decode().split("|")

        cur_windows = winlaunch.current_windows()
        for wid in cur_windows:
            if winlaunch.win_name(wid) == "IBOS Comm":
                self.ibos_wid = wid
                break

        netapps = {}
        for l in state[3].split("\n"):
            netapps[l.split(", ")[2]] = int(l.split(" ")[1][:-1])

        for l in state[2].split("\n"):
            id = int(l.split(" ")[1][:-1])
            if id == 0:
                continue
            url = l.split(", ")[1]
            ip = l.split(", ")[2]
            if id > self.last_webapp:
                self.last_webapp = id
                self.tabs[id-1] = BrowserContainer(id-1, url, 8081 + netapps[ip] - 1)
                self.hijack = True
        
        self.builder.get_object("app_combobox").config(values=[x.split(" ")[1][:-1] for x in state[2].split("\n")])
        self.builder.get_object("app_combobox").bind('<<ComboboxSelected>>', self.on_app_combobox_select)
        self.builder.get_variable("app_combobox_text").set(state[1])

        if int(state[1]) - 1 != self.cur_tab and int(state[1]) != 0:
            self.set_url_text(state[0].split(", ")[0])
            self.cur_tab = int(state[1]) - 1

            for tid in self.tabs:
                self.tabs[tid].hide()

            if self.cur_tab != -1:
                self.tabs[self.cur_tab].show()

    def set_url_text(self, url):
        self.builder.get_variable("url_entry_text").set(url)

    def on_button_send_click(self):
        new_url = self.builder.get_variable("url_entry_text").get()
        try:
            ip = socket.gethostbyname(new_url)
            print("DNS Lookup: {}".format(ip))
            self.connection.sendall(("MSG-NEW-URL|" + new_url + "|" + ip + "#").encode())
        except Exception as e:
            # TODO: WHAT DO WE DO IF THE DNS LOOKUP FAILS? prob send it to maude
            print("Exception: {}".format(str(e)))

    def on_app_combobox_select(self, event):
        new_tab = self.builder.get_object("app_combobox").get()
        self.connection.sendall(("MSG-SWITCH-TAB|" + new_tab + "#").encode())
        self.fetch_state()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    def ex():
        os.system("for i in $(ps -eaf | grep firefox | awk '{print $2}'); do kill -9 $i; done")
        app.on_exit()
    atexit.register(ex)
    app.run()
