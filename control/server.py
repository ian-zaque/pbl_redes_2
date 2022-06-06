from paho.mqtt import client as mqtt_client
import random, time

_BROKER = 'test.mosquitto.org'
_PORT = 1883
_TOPIC = '/server'

class Server:
    
    def __init__(self, ID, topic):
        self.client_id = 'server_'+ID
        self.username = 'user_'+ self.client_id
        self.password = 'senhaforte'
        # self.topic = topic
        
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(_BROKER, _PORT)
        return client
    
    def subscribe(self,client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe('lixeira')
        client.on_message = on_message
        
    def run(self):
        print('222222222222')
        client = self.connect_mqtt()
        self.subscribe(client)
        print('zzzzzzzzzz',client)
        client.loop_forever()
