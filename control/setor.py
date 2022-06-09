import json
import random
import string
from threading import Thread

from server import Server

_TOPIC = ('lixeira/', 'caminhao/')


class Setor(Server):
    
    def __init__(self, latitude: int, longitude: int):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__lixeiras = []
        Server.__init__(self, 'setor/', _TOPIC)
    
    
    def receberDados(self):
        def on_message(client, userdata, msg):
            mensagem = msg.payload
            if mensagem:
                mensagem = json.loads(mensagem)
                if 'lixeira' in msg.topic:
                    self.gerenciarLixeiras(mensagem)
                elif 'caminhao' in msg.topic:
                    self.gerenciarCaminhao(mensagem)
                else:
                    print(mensagem)
            return mensagem
        
        self._server.on_message = on_message
        self._server.loop_start()
        
    def run(self):
        self._server = self.connect_mqtt()
        Thread(target=self.receberDados).start()
            
    async def gerenciarLixeiras(self, msg):
        if 'dados' in msg:
            if 'id' in msg['dados']:     
                if (msg['id'], msg['porcentagem']) not in self.__lixeiras:
                    lixeirasId = self.__separaIds(self.__lixeiras)
                    if msg['id'] not in lixeirasId:
                        print(f"Lixeira {msg['id']} conectada")
                        self.__lixeiras.append([msg['id'], msg['porcentagem']])
                    else:
                        self.__lixeiras[lixeirasId.index(msg['id'])][1] = msg['porcentagem']
                    sorted(self.__lixeiras, key=lambda l:l[1], reverse=True) #ordeno em ordem decrescente
    
    async def gerenciarCaminhao(self, msg):
        if 'dados' in msg:
            if 'id' in msg['dados']:         
                print(f"Caminhao {msg['id']} conectado!")
   
    def __separaIds(self, lixeiras_coletar: list) -> list:
        """Organiza a ordem de coleta por parte do adm
        
        Args:
            lixeiras_coletar (list): lista de lixeiras criticas para serem coletadas

        Returns:
            list : todas as lixeiras mais criticas a serem coletadas
        """

        lista = []
        for l in lixeiras_coletar: #adiciono apenas o id na lista
            lista.append(l[0])
            
        return lista

    
setor = Setor(100, 200)
setor.run()