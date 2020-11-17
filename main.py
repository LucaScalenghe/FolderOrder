from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import logging
import shutil
from pathlib import Path
from extensions import extension_paths


def decideFolder(file_name):
    ext = getExtension(file_name)
    ext = '.' + ext
    path = Path(extension_paths[ext])
    return path


def getName(stringA):
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
    stringA = Path(stringA)
    stringB = Path(stringB)
    return stringA/stringB


class myHandler(FileSystemEventHandler):

    def __init__(self, tracked, destination):
        self.tracked = tracked
        self.destination = destination

    def on_any_event(self, event):
        for file_name in os.listdir(tracked):
            print(f"{file_name} has been moved to the destination folder!")
            i = 1
            # gives where the file is at the moment (isn't moved yet)
            original_path = unifyPath(tracked, file_name)   #is a string

            # gives me the destination path of the file
            # dest_path = unifyPath(destination,file_name)
            dest = Path(destination)
            # is a Path element that has the piece of path of the folder destinationFolderPath/folder_Path/file_name(1).extension
            folder_path = decideFolder(file_name)
           
            dest_path = dest/folder_path     # is now in the right folder now you must add the file name, number and extension

            dest_path = dest_path/Path(file_name)   #adding the filename.extension

            file_exists = os.path.isfile(dest_path)      # check if the file already exists with that name
            while file_exists:
                #destination + name + str(i) + extension   in order to not have duplicates
                i += 1
                fname = getName(file_name)
                number = str(i)
                point = '.'
                ext = getExtension(file_name)

                # creating the actual destination path adding the number
                name_with_number = Path(fname + number + point + ext)
                dest_path = dest_path/name_with_number

                # check if not true does another while loop
                file_exists = os.path.isfile(dest_path)

            # moving the file from his original path to his destination path
            dest_path = str(dest_path)
            os.rename(original_path, dest_path)


if __name__ == "__main__":

    tracked = 'C:/Users/lucas/Desktop/BucoNero'
    destination = 'C:/Users/lucas/Desktop/File'

    handler = myHandler(tracked, destination)

    obs = Observer()
    obs.schedule(handler, tracked, recursive=False)

    # start the observer thread
    obs.start()
    try:
        while True:
            print('...')
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
        obs.join()
