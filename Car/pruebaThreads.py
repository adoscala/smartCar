import threading
from VRDriver import visualRecognition
from OBDIIDriver import obdIIDriver
from multiprocessing import Queue
from random import random
import argparse
import os
from time import sleep
from collections import deque
import requests
import json

server_url = 'http://172.20.10.2:3000/'
def serialConnection():
    os.system("sudo rfcomm connect hci0 00:1D:A5:68:98:8B")

def calcular_tendencia(arr):
        suma = 0
        for i in range(0, len(arr)-1):
                derivada = arr[i+1].descripcion - arr[i].descripcion
                suma += derivada
        promedio = suma / (len(arr)-1)
        return promedio

def alert(event, historico):
        """Enviar datos al servidor"""
        url= server_url + 'eventos/crear'
        args = {
                "tipo": event.tipo,
                "descripcion": event.descripcion,
                "conductor": event.conductor,
                "hora": event.hora}
        r = requests.post(url, json=json.dumps(args))
    
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
    
    sleep(10)

    vR.start()
    
    obdII = obdIIDriver(events, events_lock)
    obdII.daemon = True
    obdII.start()

    info_queue = deque([], maxlen = 60)
   
    while True: # Loop principal del programa
        if not events.empty():
            event = events.get()
            print(event)
            # Hacer lo que haya que hacer con el evento
            if event.tipo == "INFO":
                    info_queue.append(event)
            elif event.tipo == "BLINK FREQUENCY":
                    if event.descripcion > 0.5:
			    temp_list = []
			    for j in info_queue:
				if j.subtipo == 'velocidad':
				    temp_list.append(j)
                            tendencia = calcular_tendencia(temp_list)
                            if (tendencia > 3):
                                    alert(event, temp_list)
                            #Hay que ver los cambios en la velocidad  
            elif event.tipo == "ALERT":
                    alert(event, historico)
                    #Hay que enviar el evento al servidor


