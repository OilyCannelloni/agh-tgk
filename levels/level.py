from abc import ABC, abstractmethod



class Level(ABC):
    @abstractmethod
    def load(self):
        pass


