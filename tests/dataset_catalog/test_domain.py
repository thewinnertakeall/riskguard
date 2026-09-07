import pytest

from app.dataset_catalog.domain.entities.dataset_metrics import DatasetMetrics
from app.dataset_catalog.domain.entities.dataset_source import (
    DatasetSource,
    CsvDatasetSource,
    JsonDatasetSource,
    ApiDatasetSource,
    build_dataset_source,
)


def test_csv_inherits_dataset_source():
    assert issubclass(CsvDatasetSource, DatasetSource)


def test_json_inherits_dataset_source():
    assert issubclass(JsonDatasetSource, DatasetSource)


def test_api_inherits_dataset_source():
    assert issubclass(ApiDatasetSource, DatasetSource)


def test_csv_source_validation():
    source = CsvDatasetSource("riesgos.csv")

    assert source.source_type == "csv"
    assert source.validate() is True


def test_json_source_validation():
    source = JsonDatasetSource("riesgos.json")

    assert source.source_type == "json"
    assert source.validate() is True


def test_api_source_validation():
    source = ApiDatasetSource("https://example.org/api")

    assert source.source_type == "api"
    assert source.validate() is True


def test_factory():
    source = build_dataset_source(
        "csv",
        "dataset.csv",
    )

    assert isinstance(source, CsvDatasetSource)


def test_invalid_source():
    with pytest.raises(ValueError):
        build_dataset_source(
            "csv",
            "dataset.json",
        )


def test_negative_record_count():
    with pytest.raises(ValueError):
        DatasetMetrics(-1)
