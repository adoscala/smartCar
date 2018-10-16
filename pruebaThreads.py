import threading
from VRDriver import visualRecognition
from OBDIIDriver import obdIIDriver
from multiprocessing import Queue
from random import random
import argparse
import os
from time import sleep

def serialConnection():
    os.system("sudo rfcomm connect hci0 00:1D:A5:68:98:8B")
    
if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", required=True,
            help = "path to where the face cascade resides")
    ap.add_argument("-p", "--shape-predictor", required=True,
            help="path to facial landmark predictor")
    ap.add_argument("-a", "--alarm", type=int, default=0,
            help="boolean used to indicate if TraffHat should be used")
    args = vars(ap.parse_args())

    events = Queue() #Cola de eventos
    events_lock = threading.Lock()
    vR = visualRecognition(events, events_lock, args)
    vR.daemon = True #Para que termine cuando se cierre el main
    
    serialThread = threading.Thread(target=serialConnection)
    serialThread.daemon = True
    serialThread.start()
    serialThread.join()
    
    sleep(10)

    vR.start()
    
    obdII = obdIIDriver(events, events_lock)
    obdII.daemon = True
    obdII.start()
    
    while True: # Loop principal del programa
        if not events.empty():
            event = events.get()
            print(event)
            # Hacer lo que haya que hacer con el evento

