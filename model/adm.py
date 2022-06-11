from model.client import Cliente


class Adm(Cliente):

    def __init__(self, topico):
        Cliente.__init__(self, "adm", "adm/")
        self.__lixeiras
   
    def getLixeirasByNumber(self, number: int) -> list:
        """Retorna a quantidade de lixeiras exigida

        Args:
            number (int): numero de lixeiras a ser retornado

        Returns:
            list: lista de lixeiras
        """
        # after subscribed, retrieve data from topic /lixeiras and limit by number
        if  number >= 0 and number <= len(self.__lixeiras):
            return self.__lixeiras[:number]
        return self.__lixeiras
    
    def getLixeiraByID(self, id: str) -> dict:
        """Busca uma lixera pelo id

        Args:
            id (str): id da lixera

        Returns:
            dict: dicionario contendo as informacoes de determinada lixeira 
        """
        # after subscribed, retrieve data from topic /lixeiras/id and return
        for l in self.__lixeiras:
            if id in l:
                return l
        return {}
        
    def receberDados(self):
        """Recebe a mensagem do servidor e realiza ações
        """
        while True:
            try:
                super().receberDados()
                if 'dados' in self._msg:
                    self.__lixeiras = self._msg['dados']['lixeiras']
                
            except Exception as ex:
                print("Erro ao receber dados => ", ex)
                break