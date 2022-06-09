import asyncio
import json
import random
import string
import time
from threading import Thread, local

from paho.mqtt.client import Client

_BROKER = 'test.mosquitto.org'
_PORT = 1883

class Cliente: 
    
    def __init__(self, type: str, topic: str =""):
        self._client_id = f'{type}/'+"".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self._topic = topic
        self._topicsPublish = ()
        self._msg = {'dados': '', 'acao': ''}
        self._mensagemRequest = {'dados': '', 'acao': ''}
        self._client_mqtt = Client(self._client_id)
    
    def connect_mqtt(self) -> Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Conectado ao Broker!")
            else:
                print("Falha ao se conectar, código de erro: %d\n", rc)
       
        self._client_mqtt.on_connect = on_connect
        self._client_mqtt.connect(_BROKER, _PORT)
        self._client_mqtt.subscribe(self._topic)
        
        for topic in self._topicsPublish:
            self._client_mqtt.publish(topic)
            
        return self._client_mqtt

    def receberDados(self):
        def on_message(client, userdata, msg):
            mensagem = msg.payload
            if mensagem:
                self._mensagemRequest = json.loads(mensagem)
                print(mensagem, msg.topic)
                return mensagem
            
        self._client_mqtt.on_message = on_message
        self._client_mqtt.loop_start()
    
    def enviarDados(self, topic):
        try:
            msg = json.dumps(self._msg).encode("utf-8")
            result = self._client_mqtt.publish(topic, msg)
            if result[0] == 0:
                print(f"Mensagem para o topico `{topic}`")
            else:
                print(f"Falha ao enviar mensagem para o topico {topic}")
        except Exception as ex:
            print("Não foi possivel enviar a mensagem => ", ex)
            
    def enviarDados(self):
        try:
            msg = json.dumps(self._msg).encode("utf-8")
            result = self._client_mqtt.publish(self._topic, msg)
            if result[0] == 0:
                print(f"{self._topic}  {msg}")
            else:
                print(f"Falha ao enviar mensagem para o topico {self._topic}")
        except Exception as ex:
            print("Não foi possivel enviar a mensagem => ", ex)     

    def run(self):
        self._client_mqtt = self.connect_mqtt()
        Thread(target=self.receberDados).start()
        
