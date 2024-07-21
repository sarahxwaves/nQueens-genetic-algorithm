from abc import ABC, abstractmethod

class Individuo(ABC):
    
    def __init__(self):
        self._avaliated = False
        self._eval = 0
        super().__init__()

    #crossover
    @abstractmethod
    def crossover(self, individual):
        pass
    
    #mutacao
    @abstractmethod
    def mutate(self):
        pass
    
    #fitness
    @abstractmethod
    def evaluate(self):
        pass

    def get_evaluate(self):
        if not self._avaliated:
            self._eval = self.evaluate()
            self._avaliated = True
        return  self._eval
