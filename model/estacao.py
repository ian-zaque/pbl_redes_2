from client import Client
import random, string
class Estacao(Client):

    def __init__(self):
        ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        topic = '/estacao/'+ID
        Client.__init__(self, ID, topic)
        
        print("Estação:", ID)
        print("Topic: ", topic)
