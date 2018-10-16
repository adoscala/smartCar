import threading
from VRDriver import visualRecognition
from OBDIIDriver import obdIIDriver
from queue import Queue
from random import random

    
if __name__ == "__main__":
    events = Queue() #Cola de eventos
    events_lock = threading.Lock() #No se usa, pero si hay problema de concurrencias después se solucionan con esto
    vR = visualRecognition(events, events_lock)
    vR.daemon = True #Para que termine cuando se cierre el main
    obdII = obdIIDriver(events, events_lock)
    obdII.daemon = True

    vR.start()
    obdII.start()
    
    while True: # Loop principal del programa
        if not events.empty():
            event = events.get()
            print(event)
            # Hacer lo que haya que hacer con el evento

