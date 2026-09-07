from abc import ABC, abstractmethod


class DatasetSource(ABC):
    """
    Clase base abstracta para representar el origen de un dataset.

    Demuestra herencia, abstracción y polimorfismo.
    """

    def __init__(self, location: str):
        self.location = location

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Tipo concreto de fuente."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> bool:
        """Valida la configuración de la fuente."""
        raise NotImplementedError


class CsvDatasetSource(DatasetSource):

    @property
    def source_type(self) -> str:
        return "csv"

    def validate(self) -> bool:
        return self.location.lower().endswith(".csv")


class JsonDatasetSource(DatasetSource):

    @property
    def source_type(self) -> str:
        return "json"

    def validate(self) -> bool:
        return self.location.lower().endswith(".json")


class ApiDatasetSource(DatasetSource):

    @property
    def source_type(self) -> str:
        return "api"

    def validate(self) -> bool:
        return (
            self.location.startswith("http://")
            or self.location.startswith("https://")
        )


def build_dataset_source(source_type: str, location: str) -> DatasetSource:
    """
    Factory sencilla para construir una implementación concreta.
    """

    source_type = source_type.lower()

    implementations = {
        "csv": CsvDatasetSource,
        "json": JsonDatasetSource,
        "api": ApiDatasetSource,
    }

    source_class = implementations.get(source_type)

    if source_class is None:
        raise ValueError(
            f"source_type no soportado: {source_type}"
        )

    source = source_class(location)

    if not source.validate():
        raise ValueError(
            f"Fuente inválida para tipo {source_type}: {location}"
        )

    return source
