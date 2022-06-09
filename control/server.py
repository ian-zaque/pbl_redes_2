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
    
    def publish(self):
        msg_count = 0
        for i in range(10):
            time.sleep(1)
            try:
                msg = json.dumps({'dados': {}, 'acao': 'esvaziar'}).encode("utf-8")
                result = self._server.publish(self._topics[0], msg)
                status = result[0]
                if status == 0:
                    print(f"Enviando `{msg}` para o topic `{self._topics[0]}`")
                else:
                    print(f"Failed to send message to topic {self._topics[0]}")
                msg_count += 1
            except Exception as ex:
                print("Não foi possivel enviar a mensagem => ", ex) 
            
        #self.receberDados()
        #Thread(target=self.receberDados).start()
        #self._server.loop_start()
        #self._server.on_message = self.mensagem()
        #Thread(target=self.mensagem).start()
        
        
