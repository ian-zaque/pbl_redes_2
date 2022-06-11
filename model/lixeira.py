from pydoc_data.topics import topics
from time import sleep
from client import Cliente
from random import randint
from threading import Thread, local

class Lixeira(Cliente):

    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__capacidade = randint(1,10) #m³
        self.__bloqueado = False
        self.__lixo = 0
        self.__porcentagem = 0
        Cliente.__init__(self, "lixeira", "lixeira/")
        self._topicsPublish = (f"lixeira/{self._client_id}")
        
    def dadosLixeira(self):
        """Informacoes da lixeira

        Returns:
            dict: informacoes da lixeira
        """
        if(self.__bloqueado == True):
            status = "Bloqueada"
        else:
            status = "Desbloqueada"

        return {
            "id": self._client_id,
            "latitude": self.__latitude, 
            "longitude": self.__longitude, 
            "status": status, 
            "capacidade": self.__capacidade, 
            "porcentagem": f'{self.__porcentagem:,.2f}'+'%'
        }
    
    def addLixo(self, lixo: int):
        """Adiciona lixo na lixeira até o permitido
        
        Args
            lixo: int
                quantidade de lixo adiconada
                
        Returns: 
            boolean: retorna True se conseguir adionar lixo
        """
        if(self.__capacidade >= self.__lixo + lixo): #se a capacidade de lixo nao for excedida, o lixo é adicionado
            self.__lixo += lixo
            self.__porcentagem = self.__lixo/self.__capacidade*100
            if(self.__porcentagem > 80):
                self.enviarDados(self.__topicsPublish)
            if(self.__capacidade == self.__lixo): #se a capacidade de lixo chegar ao limite, o lixo e bloqueado
                self.__bloqueado = True
                
        self._msg['dados'] = self.dadosLixeira()
        self.enviarDados()
    
    def esvaziarLixeira(self):
        """Redefine a quantidade de lixo dentro da lixeira
        """
        if(self.__bloqueado == True):
            self.__bloqueado = False
        self.__lixo = 0

        #retorna nova informacao sobre o objeto
        self._msg['dados'] = self.dadosLixeira()
        self.enviarDados()
        
        print(f"Lixeira {self._client_id} ESVAZIADA")
    
    def bloquear(self):
        """Trava a porta da lixeira
        """  
        self.__bloqueado = True
        self._msg['dados'] = self.dadosLixeira()
        self.enviarDados()
        print(f"Lixeira {self._client_id} BLOQUEADA")

    def desbloquear(self):
        """Destrava a porta da lixeira
        """
        if(self.__capacidade > self.__lixo):
            self.__bloqueado = False
            print(f"Lixeira {self._client_id} DESBLOQUEADA")
            
            #retorna nova informacao sobre o objeto
            self._msg['dados'] = self.dadosLixeira()
            self.enviarDados()
        
        else:
            print(f"Lixeira Cheia! Impossível desbloquear Lixeira {self.__id}")
    
    def generateRandomData(self):
        # options = {1: 'add', 2:'bloquear', 3:'desbloquear'}
        while self.__bloqueado == False:
            sleep(2)
            option = randint(1,3)
            
            if option == 1: self.addLixo(1)
            elif option == 2: self.bloquear()
            elif option == 3: self.desbloquear()
            
            option = 0
            sleep(3)
    
    def receberDados(self):
        """Recebe a mensagem do servidor e realiza ações
        """
        while True:
            try:
                super().receberDados()
                if('acao' in self._msg):
                    if(self._msg['acao'] == "esvaziar"):
                        print("Esvaziando Lixeira...")
                        self.esvaziarLixeira()
                    elif(self._msg['acao'] == "bloquear"):
                        print("Bloqueando Lixeira...")
                        self.bloquear()
                    elif(self._msg['acao'] == "desbloquear"):
                        print("Desbloqueando Lixeira...")
                        self.desbloquear()
            except Exception as ex:
                print("Erro ao receber dados => ", ex)
                break


lixera = Lixeira(randint(0,50), randint(0,50))
lixera.run()
Thread(target=lixera.generateRandomData).start()
