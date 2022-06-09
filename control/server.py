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
        
    def connect_mqtt(self) -> Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Servidor iniciado! {self._server_id}")
            else:
                print("Falha ao se conectar, codigo de retorno %d\n", rc)
        server = Client(self._server_id)
        server.on_connect = on_connect
        for topic in self._topics:
            server.subscribe(topic) #se inscreve numa lista de topicos
            print(topic)
        server.connect(_BROKER, _PORT)
        return server
    
    def publish(self):
        msg_count = 0
        while True:
            time.sleep(1)
            try:
                msg = json.dumps({"oláq0wq0w": 'duwh'}).encode("utf-8")
                result = self._server.publish(self._topics[0], msg)
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{self._topics[0]}`")
                else:
                    print(f"Failed to send message to topic {self._topics[0]}")
                msg_count += 1
            except Exception as ex:
                print("Não foi possivel enviar a mensagem => ", ex) 
            
   
    """def mensagem(self):
        def on_message(client, userdata, msg):
            mensagem = msg.payload.decode()
            print(f"Recebida `{mensagem}` do topico `{msg.topic}`")
            if mensagem:
                mensagem = json.loads(mensagem)
            return mensagem"""
        
    def run(self):
        self._server = self.connect_mqtt()
        self.publish()
        #self._server.on_message = self.mensagem()
        #Thread(target=self.mensagem).start()
        
        
