from client import Client
import random, string
class Adm(Client):

    def __init__(self):
        ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        topic = '/adm/'+ID
        Client.__init__(self, ID, topic)
        
        print("ADM:", ID)
        print("Topic: ", topic)