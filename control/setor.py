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
        self.__lixeiras_coletar = []
        self.__lixeiras = []
        Server.__init__(self, 'setor/', _TOPIC)
    
    def receberDados(self):
        """Recebe e gerencia as mensagens dos topicos para o qual o setor foi inscrito

        Returns:
            msg: mensagem de um determinado topico para o qual o setor se inscreveu
        """
        while True:
            def on_message(client, userdata, msg):
                mensagem = msg.payload
                if mensagem:
                    mensagem = json.loads(mensagem)
                    if 'lixeira' in msg.topic:
                        Thread(target=self.gerenciarLixeiras, args=(mensagem, )).start()
                        #self.gerenciarLixeiras(mensagem)
                    elif 'caminhao' in msg.topic:
                        Thread(target=self.gerenciarCaminhao, args=(mensagem, )).start()
                        #self.gerenciarCaminhao(mensagem)
                    else:
                        print(mensagem)
                return mensagem
            
            self._server.on_message = on_message
            self._server.loop_start()
                   
    def gerenciarLixeiras(self, msg):
        """Gerencia as mensagens enviadas para o topico lixeiras/

        Args:
            msg (dict): mensagem recebida de uma determinada lixeira
        """
        if 'dados' in msg:     
            lixeirasId = self.__separaIds(self.__lixeiras)
            #se as lixeira nao estiver na lista de lixeras, ela sera adicionada, se estiver tera seu dados atualizado
            if msg['dados']['id'] not in lixeirasId:
                print(f"\nLixeira {msg['dados']['id']} conectada")
                self.__lixeiras.append(msg['dados'])
            else:
                self.__lixeiras[lixeirasId.index(msg['dados']['id'])] = msg['dados']
                
            #verifica se a lixeira ja esta em estado critico
            if float(msg['dados']['porcentagem'][:2]) >= 75:
                lixeirasColetarId = self.__separaIds(self.__lixeiras_coletar)
                if msg['dados']['id'] not in lixeirasColetarId:
                        self.__lixeiras_coletar.append(msg['dados'])
                else:
                    self.__lixeiras_coletar[lixeirasColetarId.index(msg['dados']['id'])] = msg['dados']
                self.__lixeiras_coletar = sorted(self.__lixeiras_coletar, key=lambda l:l["porcentagem"], reverse=True)
                self.enviarDadosCaminhao()
            self.__lixeiras = sorted(self.__lixeiras, key=lambda l:l["porcentagem"], reverse=True)
            self.enviarDadosServidor()
            
    def gerenciarCaminhao(self, msg: dict):
        """Gerencia as mensagens enviadas para o topico caminhao/

        Args:
            msg (dict): mensagem recebido do caminhao
        """
        if 'acao' in msg:
            if msg['acao'] != '':
                mensagem = {'acao': 'esvaziar'}
                self.enviarDados(msg['acao'], mensagem)
   
    def enviarDadosServidor(self):
        """Envia informacoes de todas as para o topico do adm/
        """
        msg = {'dados': self.__lixeiras}
        self.enviarDados(f'adm/', msg)

    def enviarDadosCaminhao(self):
        """Envia as lixeiras a serem coletada para o tópico caminhao/
        """
        if len(self.__lixeiras_coletar):
            mensagem = {'dados': {'lixeiras': self.__lixeiras_coletar}}
            self.enviarDados('caminhao/', mensagem)
   
    def __separaIds(self, lixeiras: list) -> list:
        """Organiza a ordem de coleta por parte do adm
        
        Args:
            lixeiras_coletar (list): lista de lixeiras criticas para serem coletadas

        Returns:
            list : todas as lixeiras mais criticas a serem coletadas
        """
        lista = []
        for l in lixeiras: #adiciono apenas o id na lista
            lista.append(l['dados']['id'])
            
        return lista

    def run(self):
        """"Metodo que inicia o servidor MQTT
        """
        self._server = self.connect_mqtt()
        Thread(target=self.receberDados).start()
    
    def dadosSetor(self):
        """Informacoes da lixeira

        Returns:
            dict: informacoes da lixeira
        """
        return {
            "id": self._server_id,
            "latitude": self.__latitude, 
            "longitude": self.__longitude
        }

setor = Setor(100, 200)
setor.run()