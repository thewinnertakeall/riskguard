from app.dataset_catalog.domain.entities.dataset import Dataset
from app.dataset_catalog.domain.repositories.dataset_repository import DatasetRepository


class GetDataset:

    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def execute(self, dataset_id: int) -> Dataset | None:
        return self.repository.get(dataset_id)
