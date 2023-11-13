from abc import ABC, abstractmethod

class MassFlowController(ABC):

    @abstractmethod
    def get_flow_rate(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abstractmethod
    def set_flow_rate(self, flow_rate:float):
        raise NotImplementedError()
