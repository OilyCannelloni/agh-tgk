from abc import ABC, abstractmethod



class Level(ABC):
    @staticmethod
    @abstractmethod
    def load():
        pass

