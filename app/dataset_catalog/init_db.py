from app.database import engine

from app.dataset_catalog.infrastructure.persistence.models import (
    DatasetCatalogModel,
)


def init_dataset_catalog() -> None:
    """
    Crea exclusivamente la tabla dataset_catalog.
    No ejecuta create_all sobre todo el esquema.
    """

    DatasetCatalogModel.__table__.create(
        bind=engine,
        checkfirst=True,
    )
