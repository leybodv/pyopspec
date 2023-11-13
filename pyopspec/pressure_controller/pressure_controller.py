from abc import ABC, abstractmethod

class PressureController(ABC):

    @abstractmethod
    def get_pressure(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abstractmethod
    def set_pressure(self, pressure:float):
        raise NotImplementedError()
