import threading
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
                self.events.put(self.name)