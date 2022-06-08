from client import Client
import random, string
class Caminhao(Client):

    def __init__(self):
        ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        topic = '/caminhao/'+ID
        Client.__init__(self, ID, topic)
        
        print("Caminhão:", ID)
        print("Topic: ", topic)
