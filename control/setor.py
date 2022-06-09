from server import Server
import random, string

_TOPIC = ('lixeira/', 'caminhao/')


class Setor(Server):
    
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude
        Server.__init__(self, 'setor/', _TOPIC)
    
setor = Setor()
setor.run()