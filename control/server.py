from paho.mqtt import client as mqtt_client
import random, time

_BROKER = 'broker.emqx.io'
_PORT = 1883
_TOPIC = '/server'

class Server:
    
    def __init__(self, ID, topic):
        self.server_id = 'server_'+ID
        self.username = 'user_'+ self.server_id
        self.password = 'senhaforte'
        # self.topic = topic
        
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
                
        # Connecting Client ID
        client = mqtt_client.Client(self.server_id)
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(_BROKER, _PORT)
        return client

    def publish(self,client):
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(_TOPIC, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{_TOPIC}`")
            else:
                print(f"Failed to send message to topic {_TOPIC}")
            msg_count += 1


    def run(self):
        print('111111111')
        client = self.connect_mqtt()
        client.loop_start()
        self.publish(client)
