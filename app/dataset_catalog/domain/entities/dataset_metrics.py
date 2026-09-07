from dataclasses import dataclass


@dataclass
class DatasetMetrics:
    """
    Métricas del dataset.

    record_count representa la cantidad de registros existentes
    en la fuente. No representa registros CRUD individuales.
    """

    record_count: int = 0

    def __post_init__(self):
        if self.record_count < 0:
            raise ValueError("record_count no puede ser negativo")
