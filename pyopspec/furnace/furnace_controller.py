from abc import ABC, abstractmethod

class FurnaceController(ABC):
    """
    """

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abstractmethod
    def get_temperature(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def set_ramp_rate(self, ramp_rate:float):
        raise NotImplementedError()

    @abstractmethod
    def set_temperature(self, temperature:float):
        raise NotImplementedError()

    @abstractmethod
    def heat_up_to(self, target_temperature:float):
        raise NotImplementedError()

    @abstractmethod
    def cool_down_to(self, target_temperature:float):
        raise NotImplementedError()
