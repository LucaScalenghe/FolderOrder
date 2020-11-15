from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import logging
import json
import shutil

class myHandler(FileSystemEventHandler):
    
    # def dispatch(self, event, tracked):
    #    self.on_any_event(event, tracked)
    def __init__ (self, tracked, destination):
        self.tracked = tracked
        self.destination = destination

    def on_any_event(self,event):
         for file_name in os.listdir(tracked):
            print(f"{event.src_path} has been moved to the destination folder!")
            shutil.move(tracked + '/' + file_name, destination)

    def on_modified(self, event):
        #  for file_name in os.listdir(tracked):
        #     print(f"{event.src_path} has been moved to the destination folder!")
        #     shutil.move(tracked + '/' + file_name, tracked)
        print('modified')
    


if __name__ == "__main__":


    tracked = 'C:/Users/lucas/Desktop/Test'
    destination = 'C:/Users/lucas/Desktop/Arrivo'

    handler = myHandler(tracked, destination)


    obs = Observer()
    obs.schedule(handler,tracked,recursive = False)

     #start the observer thread
    obs.start()
    try:
        while True:
            print('...')
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
        obs.join()





