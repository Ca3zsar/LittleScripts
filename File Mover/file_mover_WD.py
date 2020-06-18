import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

sourceFolder = "C:\\Users\\cezar\\Desktop\\source"
destinationFolder = "C:\\Users\\cezar\\Desktop\\destination"

class MyHandler(LoggingEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(sourceFolder):
            src = sourceFolder + '\\' + filename
            dest = destinationFolder + "\\" + filename
            os.rename(src,dest)
            
            
eventHandler = MyHandler()
observer = Observer()
observer.schedule(eventHandler,sourceFolder,recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
    
observer.join()

    