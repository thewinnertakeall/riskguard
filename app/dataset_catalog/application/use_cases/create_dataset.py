from app.dataset_catalog.domain.entities.dataset import Dataset
from app.dataset_catalog.domain.entities.dataset_metrics import DatasetMetrics
from app.dataset_catalog.domain.entities.dataset_source import build_dataset_source
from app.dataset_catalog.domain.repositories.dataset_repository import DatasetRepository


class CreateDataset:

    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def execute(
        self,
        code: str,
        name: str,
        description: str,
        source_type: str,
        source_location: str,
        record_count: int,
        active: bool,
    ) -> Dataset:

        source = build_dataset_source(
            source_type,
            source_location,
        )

        dataset = Dataset(
            id=None,
            code=code,
            name=name,
            description=description,
            source=source,
            metrics=DatasetMetrics(record_count),
            active=active,
        )

        return self.repository.create(dataset)
