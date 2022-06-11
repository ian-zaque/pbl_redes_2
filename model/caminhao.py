from math import dist
import random, string
from time import sleep

from client import Cliente


class Caminhao(Cliente):

    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__capacidade = 10000 #m³
        self.__lixeiras_coletar = []
        Cliente.__init__(self, "caminhao", "caminhao/")
    
    def dadosCaminhao(self):
        """Informacoes da lixeira

        Returns:
            dict: informacoes da lixeira
        """

        return {
            "id": self._client_id,
            "latitude": self.__latitude, 
            "longitude": self.__longitude
        }
        
    def __lixeiraMaisProxima(self, lixeiras_coletar: list):
        """Seleciona a lixeira mais proxima do caminhao

        Args:
            lixeiras_coletar (list): lista de lixeiras criticas para serem coletadas

        Returns:
            str : id da lixeira
        """
        lixeira_mais_prox = lixeiras_coletar[0]
        a = (self.__latitude, self.__longitude) #localizacao do caminhao

        for l in lixeiras_coletar:    
            b = (l['latitude'], l['longitude'])
            c = (lixeira_mais_prox['latitude'], lixeira_mais_prox['latitude'])
            
            if (dist(a, b) < dist(a, c)):
                lixeira_mais_prox = l
                
        return lixeira_mais_prox
    
    def coletarLixeira(self):
        """
        Esvazia a lixeira
            @param lixeira: Lixera
                lixeira a ser esvaziada
        """ 
        
        #Procura dentre as lixeras mais cheias a mais proxima
        lixeira = self.__lixeiras_coletar.pop(0)
        
        print(f"O Caminhão {self._client_id} está coletando a lixeira {lixeira['id']}")
        
        self._msg['acao'] = f"lixeiras/{lixeira['id']}"

        sleep(5)
        self.enviarDados()
        self.__latitude = lixeira['latitude']
        self.__latitude = lixeira['longetude']
        self._msg['dados']['caminhao'] = self.dadosCaminhao()
        self._msg['acao'] = ''
        self.enviarDados()
        
    def receberDados(self):
        """Recebe a mensagem do servidor e realiza ações
        """
        

    def run(self):
        super().run()
        if len(self.__lixeiras_coletar) > 0:
            self.coletarLixeira()