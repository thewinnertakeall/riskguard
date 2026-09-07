from app.dataset_catalog.domain.entities.dataset import Dataset
from app.dataset_catalog.domain.entities.dataset_metrics import DatasetMetrics
from app.dataset_catalog.domain.entities.dataset_source import build_dataset_source
from app.dataset_catalog.domain.repositories.dataset_repository import DatasetRepository
from app.dataset_catalog.infrastructure.persistence.models import DatasetCatalogModel


class SqlDatasetRepository(DatasetRepository):

    def __init__(self, db):
        self.db = db

    @staticmethod
    def _to_domain(model: DatasetCatalogModel) -> Dataset:
        source = build_dataset_source(
            model.source_type,
            model.source_location,
        )

        return Dataset(
            id=model.id,
            code=model.code,
            name=model.name,
            description=model.description,
            source=source,
            metrics=DatasetMetrics(model.record_count),
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create(self, dataset: Dataset) -> Dataset:

        model = DatasetCatalogModel(
            code=dataset.code,
            name=dataset.name,
            description=dataset.description,
            source_type=dataset.source.source_type,
            source_location=dataset.source.location,
            record_count=dataset.metrics.record_count,
            active=dataset.active,
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._to_domain(model)

    def get(self, dataset_id: int) -> Dataset | None:

        model = (
            self.db.query(DatasetCatalogModel)
            .filter(DatasetCatalogModel.id == dataset_id)
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list(self) -> list[Dataset]:

        models = (
            self.db.query(DatasetCatalogModel)
            .order_by(DatasetCatalogModel.id)
            .all()
        )

        return [
            self._to_domain(model)
            for model in models
        ]

    def update(
        self,
        dataset_id: int,
        dataset: Dataset,
    ) -> Dataset | None:

        model = (
            self.db.query(DatasetCatalogModel)
            .filter(DatasetCatalogModel.id == dataset_id)
            .first()
        )

        if model is None:
            return None

        model.name = dataset.name
        model.description = dataset.description
        model.source_type = dataset.source.source_type
        model.source_location = dataset.source.location
        model.record_count = dataset.metrics.record_count
        model.active = dataset.active

        self.db.commit()
        self.db.refresh(model)

        return self._to_domain(model)

    def delete(self, dataset_id: int) -> bool:

        model = (
            self.db.query(DatasetCatalogModel)
            .filter(DatasetCatalogModel.id == dataset_id)
            .first()
        )

        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()

        return True
