import random
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'user'
password = 'senhaforte'

class Client:
    
    def __init__(self, Host = '127.0.0.1', Port = 50000):
        self._Host = Host
        self._Port =  Port
        
    def connect_mqtt(self,) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client
    
    def subscribe(self,client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(topic)
        client.on_message = on_message
        
    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()
        

client = Client('127.0.0.1',500000)
client.run()
