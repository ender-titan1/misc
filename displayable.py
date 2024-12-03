from abc import ABC, abstractmethod

class Displayable(ABC):
    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass