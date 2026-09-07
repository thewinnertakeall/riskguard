from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.risk import Risk


class RiskRepository(ABC):

    @abstractmethod
    def find_by_id(self, risk_id: int) -> Optional[Risk]:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Risk]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Risk]:
        raise NotImplementedError

    @abstractmethod
    def save(self, risk: Risk) -> Risk:
        raise NotImplementedError
