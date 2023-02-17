# Created by Ian # Created by Ian
from abc import ABC, abstractmethod

# Interface for drawable objects
class Collectable(ABC):
    @abstractmethod
    def Draw(self):
        pass