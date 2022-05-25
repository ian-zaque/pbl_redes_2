from client import Client

class Estacao(Client):

    def __init__(self, id, HOST= '127.0.0.1'):
        Client.__init__(self, HOST, 50000)
        self.__id = id
