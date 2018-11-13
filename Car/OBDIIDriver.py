import threading
from random import random
import obd
from time import sleep
from Evento import Evento
import RPi.GPIO as GPIO

class obdIIDriver(threading.Thread):
    # aca va todo lo relacionado a obdII

    def __init__(self, events, lock):
        threading.Thread.__init__(self)
        self.events = events
        self.lock = lock
        self.connection = obd.OBD()

    def run(self):
        try:
            print self.connection.is_connected()
            while True:
                response1 = self.connection.query(obd.commands.SPEED)
                response2 = self.connection.query(obd.commands.RPM)
                self.events.put(Evento("INFO", "rpm", response2.value.magnitude, {"nombre":"Paula","apellido":"Rios","matricula":"HAA122"}))
                self.events.put(Evento("INFO", "velocidad", response1.value.magnitude, {"nombre":"Paula","apellido":"Rios","matricula":"HAA122"}))
                sleep(1)
        except:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(3, GPIO.OUT)
            GPIO.output(3, True)
            
