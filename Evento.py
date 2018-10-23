import datetime

class Evento:

    def __init__(self, tipo, descripcion, conductor):
        self.tipo = tipo
        self.descripcion = descripcion
        self.hora = datetime.datetime.now()
        self.conductor = conductor