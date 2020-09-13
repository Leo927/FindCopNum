from gui import myGUI
import tkinter as tk
import threading
import logging
import time
from TreeBuilder import TreeBuilder

def worker():
    # Skeleton worker function, runs in separate thread (see below)   
    while True:
        # Report time / date at 2-second intervals
        time.sleep(2)
        timeStr = time.asctime()
        msg = 'Current time: ' + timeStr
        logging.info(msg) 
def main():
    root = tk.Tk()
    if __name__ == '__main__':
        myGUI(root)



main()