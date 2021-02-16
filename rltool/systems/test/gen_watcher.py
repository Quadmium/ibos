# You'll need to pip install watchdog

import os
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

class Watcher:
    DIRECTORY_TO_WATCH = get_script_path()

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        print("{} Refreshing...".format(datetime.now().strftime("%H:%M:%S")))
        exec(open("./gen.py").read())

if __name__ == '__main__':
    w = Watcher()
    w.run()