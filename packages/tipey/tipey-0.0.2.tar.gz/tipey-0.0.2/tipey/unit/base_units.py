from abc import ABCMeta, abstractmethod

class u(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def quantity():
        pass

    @staticmethod
    @abstractmethod
    def d():
        pass