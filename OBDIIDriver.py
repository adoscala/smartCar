import threading
from random import random

class obdIIDriver(threading.Thread):
    # aca va todo lo relacionado a obdII

    def __init__(self, events, lock):
        threading.Thread.__init__(self)
        self.events = events
        self.lock = lock

    def run(self):
        while True:
            if random() < 0.15:
                self.events.put(self.name)