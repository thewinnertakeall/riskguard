from dataclasses import dataclass
from datetime import datetime

from .dataset_metrics import DatasetMetrics
from .dataset_source import DatasetSource


@dataclass
class Dataset:
    """
    Entidad principal del catálogo.

    El catálogo administra METADATOS de datasets,
    no los registros internos de external_risk_data.
    """

    id: int | None
    code: str
    name: str
    description: str
    source: DatasetSource
    metrics: DatasetMetrics
    active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
