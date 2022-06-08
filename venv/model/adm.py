from model.client import Client
import random, string, json


class Adm(Client):

    def __init__(self):
        ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        topic = '/adm/'+ID
        Client.__init__(self, ID, topic)
        
        print("ADM:", ID)
        print("Topic: ", topic)
   
    def getLixeirasByNumber(number: int):
        # after subscribed, retrieve data from topic /lixeiras and limit by number
        return str(number) + ' lixeiras pedidas'
    
    def getLixeiraByID(id):
        # after subscribed, retrieve data from topic /lixeiras/id and return
        return 'Lixeira de ID: ' + str(id)
        