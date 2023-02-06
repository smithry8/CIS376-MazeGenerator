from abc import ABC, abstractmethod
class Updateable(ABC):
    @abstractmethod
    def Update(self):
        pass