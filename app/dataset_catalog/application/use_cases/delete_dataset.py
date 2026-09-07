from app.dataset_catalog.domain.repositories.dataset_repository import DatasetRepository


class DeleteDataset:

    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def execute(self, dataset_id: int) -> bool:
        return self.repository.delete(dataset_id)
