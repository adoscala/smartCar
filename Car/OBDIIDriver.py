import threading
from random import random
import obd
from time import sleep
from Evento import Evento

class obdIIDriver(threading.Thread):
    # aca va todo lo relacionado a obdII

    def __init__(self, events, lock):
        threading.Thread.__init__(self)
        self.events = events
        self.lock = lock
        self.connection = obd.OBD()

    def run(self):
        print self.connection.is_connected()
        while True:
            response1 = self.connection.query(obd.commands.SPEED)
	    response2 = self.connection.query(obd.commands.RPM)
	    self.events.put(Evento("INFO", "rpm", response2.value.magnitude, "DEMO"))
            self.events.put(Evento("INFO", "velocidad", response1.value.magnitude, "DEMO"))
            sleep(1)
