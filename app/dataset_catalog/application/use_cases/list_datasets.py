from app.dataset_catalog.domain.entities.dataset import Dataset
from app.dataset_catalog.domain.repositories.dataset_repository import DatasetRepository


class ListDatasets:

    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def execute(self) -> list[Dataset]:
        return self.repository.list()
