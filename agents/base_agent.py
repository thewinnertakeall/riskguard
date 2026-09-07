from abc import ABC, abstractmethod
from typing import Generic, TypeVar


Context = TypeVar("Context")
Result = TypeVar("Result")


class BaseAgent(ABC, Generic[Context, Result]):

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def analyze(self, context: Context) -> Result:
        raise NotImplementedError
