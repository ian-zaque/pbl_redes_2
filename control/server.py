from paho.mqtt import client as mqtt_client
import random, time

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'user'
password = 'senhaforte'


class Server:
    
    def __init__(self, HOST = '127.0.0.1', PORT = 50000):
        self.host = HOST
        self.port = PORT
        
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
                
        # Set Connecting Client ID
        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

    def publish(self,client):
        msg_count = 0
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1


    def run(self):
        client = self.connect_mqtt()
        client.loop_start()
        self.publish(client)
        

server = Server('127.0.0.1',500000)
server.run()