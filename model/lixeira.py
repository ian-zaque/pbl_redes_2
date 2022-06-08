from client import Client
import random, string

class Lixeira(Client):

    def __init__(self, latitude, longitude):
        ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        topic = '/lixeira/'+ID
        self.__ID = ID
        self.__latitude = latitude
        self.__longitude = longitude
        self.__capacidade = 10 #m³
        self.__bloqueado = False
        self.__lixo = 0
        
        Client.__init__(self, ID, topic)
        self._msg['id'] = self.__ID
        self._msg['objeto'] = self.dadosLixeira()
        
        print("Lixeira:", ID)
        print("Topic: ", topic)
        
    def dadosLixeira(self):
        if(self.__bloqueado == True):
            status = "Bloqueada"
        else:
            status = "Desbloqueada"

        return {
            "latitude": self.__latitude, 
            "longitude": self.__longitude, 
            "status": status, 
            "capacidade": self.__capacidade, 
            "porcentagem": f'{self.getPorcentagem()*100:.2f}'+'%'
        }
    
    
    def addLixo(self, lixo: int):
        """
        Adiciona lixo na lixeira até o permitido
            @param lixo: int
                quantidade de lixo adiconada
            @return: boolean
                retorna True se conseguir adionar lixo
        """
        if(self.__capacidade >= self.__lixo + lixo): #se a capacidade de lixo nao for excedida, o lixo é adicionado
            self.__lixo += lixo
            
            if(self.__capacidade == self.__lixo): #se a capacidade de lixo chegar ao limite, o lixo e bloqueado
                self.__bloqueado = True
                
        self._msg['objeto'] = self.dadosLixeira()
        self._msg['acao'] = 'addLixo'
        self.enviarDados()
    
    def esvaziarLixeira(self):
        """
        Redefine a quantidade de lixo dentro da lixeira
        """
        if(self.__bloqueado == True):
            self.__bloqueado = False
        self.__lixo = 0

        #retorna nova informacao sobre o objeto
        self._msg['objeto'] = self.dadosLixeira()
        self._msg['acao'] = 'removeLixo'
        self.enviarDados()
        
        print(f"Lixeira {self.__ID} ESVAZIADA")
    
    def bloquear(self):
        """
        Trava a porta da lixeira
        """  
        self.__bloqueado = True
        self._msg['objeto'] = self.dadosLixeira()
        self._msg['acao'] = 'blockLixo'
        self.enviarDados()
        print(f"Lixeira {self.__id} BLOQUEADA")

    def desbloquear(self):
        """
        Destrava a porta da lixeira
        """
        if(self.__capacidade > self.__lixo):
            self.__bloqueado = False
            print(f"Lixeira {self.__id} DESBLOQUEADA")
            
            #retorna nova informacao sobre o objeto
            self._msg['objeto'] = self.dadosLixeira()
            self._msg['acao'] = 'unblockLixo'
            self.enviarDados()
        
        else:
            print(f"Lixeira Cheia! Impossível desbloquear Lixeira {self.__id}")
    
    def getPorcentagem(self):
        return self.__lixo/self.__capacidade
        
    def getId(self):
        """
        Retorna ID da lixeira
            @return latitude - str
        """
        return self.__id
 
    def getLatitude(self):
        """
        Retorna a latitude da lixeira
            @return latitude - int
        """
        return self.__latitude
    
    def getLongitude(self):
        """
        Retorna a longitude da lixeira
            @return logitude - int
        """
        return self.__longitude
 
    def getPorcentagem(self):
        """
        Retorna a porcentagem de lixo da lixeira
            @return porcentagem - float
        """
        return self.__lixo/self.__capacidade
 
    def getLixo(self):
        """
        Retorna o lixo da lixeira
            @return lixo - int
        """
        return self.__lixo
 
    def getCapacidade(self):
        """
        Retorna a capacidade da lixeira
            @return capacidade - float
        """
        return self.__capacidade
    
    def getBloqueado(self):
        """
        Retorna o status da lixeira
            @return bloquado - boolean
        """
        return self.__bloqueado    
    
lixera = Lixeira(150, 200)
lixera.run()
lixera.addLixo(1)
lixera.addLixo(1)
lixera.addLixo(4)
lixera.addLixo(1)
lixera.addLixo(1)
lixera.esvaziarLixeira()