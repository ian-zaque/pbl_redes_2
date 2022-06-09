from math import dist
import random, string

from client import Cliente


class Caminhao(Cliente):

    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__capacidade = 10000 #m³
        self.__lixeiras_coletar = []
        Cliente.__init__(self, "caminhao", "caminhao/")
        
    def __lixeiraMaisProxima(self, lixeiras_coletar: list) -> str:
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
                
        return lixeira_mais_prox["id"]
    