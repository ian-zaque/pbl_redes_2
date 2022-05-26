from client import Client
import random, string

class Lixeira(Client):

    def __init__(self):
        ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        topic = '/lixeira/'+ID
        Client.__init__(self, ID, topic)
        
        print("Lixeira:", ID)
        print("Topic: ", topic)
        
lixera = Lixeira()
lixera.run()