import json
from pydoc_data.topics import topics
import random
import string
import time

from paho.mqtt.client import Client
from threading import Thread

_BROKER = 'test.mosquitto.org'
_PORT = 1883

class Server():
    
    def __init__(self, topic: str, topics: tuple):
        self._server_id = topic+"".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self._topics = topics
        self._server = Client(self._server_id)
        
    def connect_mqtt(self) -> Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Servidor iniciado! {self._server_id}")
            else:
                print("Falha ao se conectar, codigo de retorno %d\n", rc)
        
        self._server.on_connect = on_connect
        self._server.connect(_BROKER, _PORT)
        print("Topicos: ", self._topics)
        for topic in self._topics:
            print("inscreveu-se no topico: ", topic)
            self._server.publish(topic)
            self._server.subscribe(topic+"#") #se inscreve numa lista de topicos para todas
        return self._server
    
    def enviarDados(self, topic, msg: dict):
        try:
            msg = json.dumps(msg).encode("utf-8")
            result = self._server.publish(topic, msg)
            if result[0] != 0:
                raise Exception("Mensagem não enviada para o topico "+"'"+topic+"'")
        except Exception as ex:
            print(ex)