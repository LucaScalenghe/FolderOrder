from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import logging
import json
import shutil
from pathlib import Path


def getPathName(stringA):
    a = Path(stringA)
    ris = a.name
    ris = ris.split('.')
    return ris[0]

def getExtension(stringA):
    a = Path(stringA)
    ris = a.name
    ris = ris.split('.')
    return ris[1]

def unifyPath(stringA, stringB):
    stringA= Path(stringA)
    stringB = Path(stringB)
    return stringA/stringB


class myHandler(FileSystemEventHandler):

    def __init__ (self, tracked, destination):
        self.tracked = tracked
        self.destination = destination

    def on_any_event(self,event):
         for file_name in os.listdir(tracked):
            print(f"{file_name} has been moved to the destination folder!")
            i=1
            destpath = unifyPath(destination,file_name) #gives me the destination path of the file
            
            #here i control if the file already exists with that name
            file_exists = os.path.isfile(unifyPath(destination, file_name))
            while file_exists:
                i+=1
                # I have to add the version number of the file to not have duplicates
                #destination + name + str(i) + extension
                dest = Path(destination)
                fname = getPathName(file_name)
                number = str(i)
                point = '.'
                ext = getExtension(file_name)
                
                # creating the actual destination path 
                filepath =  Path(fname + number + point + ext)
                destpath=dest/filepath
               
                #qua ricontrollo se esiste perchè se esiste rifaccio il ciclo
                file_exists = os.path.isfile(destpath)
            
            #qua devo spostarlo ATTENZIONE CHE IN FILE NAME DEVE ANDARE ANCHE IL numero e anche quando non ho aggiungo 
            #nessun numero
            os.rename(unifyPath(tracked,file_name), destpath)

    






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





