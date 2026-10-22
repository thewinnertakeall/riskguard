from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all RiskGuard agents.
    """

    def __init__(self, name: str):

        self._name = name

    @property
    def name(self) -> str:

        return self._name

    @abstractmethod
    def analyze(self, context: dict) -> dict:
        """
        Execute agent analysis.
        """
        pass
