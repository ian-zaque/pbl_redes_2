from server import Server
import random, string

class Setor(Server):
    
    def __init__(self):
        ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        topic = '/setor/'+ID
        Server.__init__(self, ID, topic)
        
        print("Setor:", ID)
        print("Topic: ", topic)
        

setor = Setor()
setor.run()