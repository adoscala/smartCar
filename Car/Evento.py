import datetime

class Evento:

    def __init__(self, tipo, subtipo, descripcion, conductor):
        self.tipo = tipo
        self.subtipo = subtipo
        self.descripcion = descripcion
        self.hora = datetime.datetime.now()
        self.conductor = conductor


