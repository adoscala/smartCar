import threading
from queue import Queue
from random import random


class visualRecognition(threading.Thread):
    # aca va todo el codigo de visual recognition

    def __init__(self, events, lock):
        threading.Thread.__init__(self)
        self.events = events
        self.lock = lock

    def run(self):
        while True:
            if random() < 0.15:
                events.put(self.name)


class obdIIDriver(threading.Thread):
    # aca va todo lo relacionado a obdII

    def __init__(self, events, lock):
        threading.Thread.__init__(self)
        self.events = events
        self.lock = lock

    def run(self):
        while True:
            if random() < 0.15:
                events.put(self.name)


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

