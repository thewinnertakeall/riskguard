from app.dataset_catalog.domain.entities.dataset import Dataset
from app.dataset_catalog.domain.entities.dataset_metrics import DatasetMetrics
from app.dataset_catalog.domain.entities.dataset_source import build_dataset_source
from app.dataset_catalog.domain.repositories.dataset_repository import DatasetRepository


class UpdateDataset:

    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def execute(
        self,
        dataset_id: int,
        current: Dataset,
        name: str | None = None,
        description: str | None = None,
        source_type: str | None = None,
        source_location: str | None = None,
        record_count: int | None = None,
        active: bool | None = None,
    ) -> Dataset | None:

        new_source_type = source_type or current.source.source_type
        new_location = source_location or current.source.location

        source = build_dataset_source(
            new_source_type,
            new_location,
        )

        updated = Dataset(
            id=current.id,
            code=current.code,
            name=name if name is not None else current.name,
            description=(
                description
                if description is not None
                else current.description
            ),
            source=source,
            metrics=DatasetMetrics(
                record_count
                if record_count is not None
                else current.metrics.record_count
            ),
            active=active if active is not None else current.active,
            created_at=current.created_at,
            updated_at=current.updated_at,
        )

        return self.repository.update(dataset_id, updated)
