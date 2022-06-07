import time
from paho.mqtt import client as mqtt_client


_BROKER = 'test.mosquitto.org'
_PORT = 1883
# _TOPIC = 'lixeira'

class Client:
    
    def __init__(self, ID, topic):
        self.server_id = 'client_'+ID
        self.username = 'user_'+ self.server_id
        self.password = 'senhaforte'
        self.topic = topic
        self._msg = {'acao': '', 'id': ''}
        self.MQTT_CLIENT = None
    
    def getID(self):
        return self.server_id
    
    def getTopic(self):
        return self.topic
    
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
                
        # Connecting Client ID
        self.MQTT_CLIENT = mqtt_client.Client(self.server_id)
        self.MQTT_CLIENT.username_pw_set(self.username, self.password)
        self.MQTT_CLIENT.on_connect = on_connect
        self.MQTT_CLIENT.connect(_BROKER, _PORT)
        return self.MQTT_CLIENT

    # def publish(self,client):
    #     msg_count = 0
    #     while True:
    #         time.sleep(1)
    #         msg = f"messages: {msg_count}"
    #         result = client.publish(self.topic, msg)
    #         # result: [0, 1]
    #         status = result[0]
    #         if status == 0:
    #             print(f"Send `{msg}` to topic `{self.topic}`")
    #         else:
    #             print(f"Failed to send message to topic {self.topic}")
    #         msg_count += 1


    def run(self):
        print('111111111')
        self.MQTT_CLIENT = self.connect_mqtt()
        self.MQTT_CLIENT.loop_start()
        print('aaaaaaaaaaaa',self.MQTT_CLIENT)
        self.enviarDados()
    
    def enviarDados(self):
        """
        Envia dados para o servidor
            @param msg: str
                mensagem que sera enviada para o servidor
        """
        try:
            msg = str(self._msg)
            result = self.MQTT_CLIENT.publish(self.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(msg)
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
        except Exception as ex:
            print("Não foi possivel enviar a mensagem => ", ex) 