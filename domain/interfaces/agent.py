from abc import ABC, abstractmethod


class Agent(ABC):
    """
    Base interface for polymorphic RiskGuard agents.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def analyze(self, context: dict) -> dict:
        pass
