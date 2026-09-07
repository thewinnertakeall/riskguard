from app.dataset_catalog.application.use_cases.create_dataset import CreateDataset
from app.dataset_catalog.application.use_cases.delete_dataset import DeleteDataset
from app.dataset_catalog.application.use_cases.get_dataset import GetDataset
from app.dataset_catalog.application.use_cases.list_datasets import ListDatasets
from app.dataset_catalog.application.use_cases.update_dataset import UpdateDataset
from app.dataset_catalog.domain.entities.dataset import Dataset


class FakeRepository:

    def __init__(self):
        self.data = {}
        self.next_id = 1

    def create(self, dataset):
        dataset.id = self.next_id
        self.next_id += 1
        self.data[dataset.id] = dataset
        return dataset

    def get(self, dataset_id):
        return self.data.get(dataset_id)

    def list(self):
        return list(self.data.values())

    def update(self, dataset_id, dataset):
        if dataset_id not in self.data:
            return None

        self.data[dataset_id] = dataset
        return dataset

    def delete(self, dataset_id):
        if dataset_id not in self.data:
            return False

        del self.data[dataset_id]
        return True


def test_crud_use_cases():

    repository = FakeRepository()

    create = CreateDataset(repository)

    dataset = create.execute(
        code="TEST-001",
        name="Dataset de prueba",
        description="Prueba",
        source_type="csv",
        source_location="test.csv",
        record_count=100,
        active=True,
    )

    assert dataset.id == 1
    assert dataset.metrics.record_count == 100

    get = GetDataset(repository)

    found = get.execute(1)

    assert found is not None
    assert found.code == "TEST-001"

    listing = ListDatasets(repository).execute()

    assert len(listing) == 1

    updated = UpdateDataset(repository).execute(
        dataset_id=1,
        current=found,
        name="Dataset actualizado",
        record_count=200,
    )

    assert updated.name == "Dataset actualizado"
    assert updated.metrics.record_count == 200

    deleted = DeleteDataset(repository).execute(1)

    assert deleted is True
    assert GetDataset(repository).execute(1) is None
