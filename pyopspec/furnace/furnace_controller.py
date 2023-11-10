from abc import ABC, abstractmethod

class FurnaceController(ABC):
    """
    """

    @abstractmethod
    def get_temperature(self) -> float:
        pass
