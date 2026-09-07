from abc import ABC, abstractmethod
from typing import Any


class SemanticRepository(ABC):
    """
    Port for semantic knowledge access.

    The domain/application layers depend on this abstraction,
    not on RDFLib, SPARQL or concrete RDF storage.
    """

    @abstractmethod
    def find_risk(self, code: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def find_critical_risks(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_causes(self, risk_uri: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_controls(self, risk_uri: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_incidents(self, risk_uri: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_inferred_status(self, risk_uri: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_graph_status(self) -> dict:
        raise NotImplementedError
