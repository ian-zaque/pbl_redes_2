from client import Cliente
import random, string

class Lixeira(Cliente):

    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__capacidade = 10 #m³
        self.__bloqueado = False
        self.__lixo = 0
        Cliente.__init__(self, "lixeira", "lixeira/")
        
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
            "porcentagem": f'{self.__lixo/self.__capacidade*100:.2f}'+'%'
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
            
            if(self.__capacidade == self.__lixo): #se a capacidade de lixo chegar ao limite, o lixo e bloqueado
                self.__bloqueado = True
                
        self._msg['response'] = self.dadosLixeira()
        self.enviarDados()
    
    def esvaziarLixeira(self):
        """Redefine a quantidade de lixo dentro da lixeira
        """
        if(self.__bloqueado == True):
            self.__bloqueado = False
        self.__lixo = 0

        #retorna nova informacao sobre o objeto
        self._msg['response'] = self.dadosLixeira()
        self.enviarDados()
        
        print(f"Lixeira {self.__ID} ESVAZIADA")
    
    def bloquear(self):
        """Trava a porta da lixeira
        """  
        self.__bloqueado = True
        self._msg['response'] = self.dadosLixeira()
        self.enviarDados()
        print(f"Lixeira {self.__id} BLOQUEADA")

    def desbloquear(self):
        """Destrava a porta da lixeira
        """
        if(self.__capacidade > self.__lixo):
            self.__bloqueado = False
            print(f"Lixeira {self.__id} DESBLOQUEADA")
            
            #retorna nova informacao sobre o objeto
            self._msg['response'] = self.dadosLixeira()
            self.enviarDados()
        
        else:
            print(f"Lixeira Cheia! Impossível desbloquear Lixeira {self.__id}")
    
    def receberDados(self):
        """Recebe a mensagem do servidor e realiza ações
        """
        try:
            mensagem = super().receberDados()
            print('MENSAGEM: ', mensagem)
            if(mensagem):
                if(mensagem['request'] == "esvaziar"):
                    print("Esvaziando Lixeira...")
                    self.esvaziarLixeira()
                elif(mensagem['request'] == "bloquear"):
                    print("Bloqueando Lixeira...")
                    self.bloquear()
                elif(mensagem['request'] == "desbloquear"):
                    print("Desbloqueando Lixeira...")
                    self.desbloquear()
        except Exception as ex:
            print("Erro ao receber dados => ", ex)
            
    """def run(self):
        self._client_mqtt = self.connect_mqtt()
        self.receberDados()
        #Thread(target=self.receberDados).start()
        self._client_mqtt.loop_forever()"""
    
lixera = Lixeira(150, 200)
lixera.run()
