from abc import ABC, abstractmethod

from app.dataset_catalog.domain.entities.dataset import Dataset


class DatasetRepository(ABC):

    @abstractmethod
    def create(self, dataset: Dataset) -> Dataset:
        raise NotImplementedError

    @abstractmethod
    def get(self, dataset_id: int) -> Dataset | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Dataset]:
        raise NotImplementedError

    @abstractmethod
    def update(self, dataset_id: int, dataset: Dataset) -> Dataset | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, dataset_id: int) -> bool:
        raise NotImplementedError
