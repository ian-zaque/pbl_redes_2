import json
import random
import string
from threading import Thread
import time

from paho.mqtt.client import Client

_BROKER = 'test.mosquitto.org'
_PORT = 1883

class Cliente: 
    
    def __init__(self, type: str, topic=""):
        self._client_id = f'/{type}/'.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        self._topic = topic
        self._msg = {'request': '', 'response': ''}
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

        return self._client_mqtt

    def receberDados(self):
        def on_message(client, userdata, msg):
            mensagem = msg.payload
            if mensagem:
                mensagem = json.loads(mensagem)
                print(mensagem)
                return mensagem
            
        self._client_mqtt.on_message = on_message

    def run(self):
        self._client_mqtt = self.connect_mqtt()
        self.receberDados()
        #Thread(target=self.receberDados).start()
        self._client_mqtt.loop_forever()

    
    """def enviarDados(self):
        try:
            msg = str(self._msg)
            result = self._client_mqtt.publish(self._topic, msg)
            status = result[0]
            if status == 0:
                print(msg)
                print(f"Enviando mensagem para o topico `{self._topic}`")
            else:
                print(f"Falha ao enviar mensagem para o topico {self._topic}")
        except Exception as ex:
            print("Não foi possivel enviar a mensagem => ", ex) """
