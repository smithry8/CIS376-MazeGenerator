from abc import ABC, abstractmethod
# interface for updateable objects
class Updateable(ABC):
    @abstractmethod
    def Update(self):
        pass