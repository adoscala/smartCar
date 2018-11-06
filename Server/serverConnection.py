import requests


server_url = "179.27.96.73:3000/eventos/crear"

def sendEvent(event):
    data = {"tipo": event.tipo, "descripcion": event.descripcion, "conductor": event.conductor, "hora": event.hora}
    r = requests.post(server_url, data=data)
    return r.status_code