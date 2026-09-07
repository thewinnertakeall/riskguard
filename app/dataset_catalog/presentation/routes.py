from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.dataset_catalog.application.dto.dataset_dto import (
    DatasetCreateDTO,
    DatasetResponseDTO,
    DatasetUpdateDTO,
)

from app.dataset_catalog.application.use_cases.create_dataset import (
    CreateDataset,
)

from app.dataset_catalog.application.use_cases.get_dataset import (
    GetDataset,
)

from app.dataset_catalog.application.use_cases.list_datasets import (
    ListDatasets,
)

from app.dataset_catalog.application.use_cases.update_dataset import (
    UpdateDataset,
)

from app.dataset_catalog.application.use_cases.delete_dataset import (
    DeleteDataset,
)

from app.dataset_catalog.infrastructure.persistence.dataset_repository_sql import (
    SqlDatasetRepository,
)

from app.dataset_catalog.init_db import init_dataset_catalog


router = APIRouter(
    prefix="/api/datasets",
    tags=["Dataset Catalog"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.on_event("startup")
def startup_dataset_catalog():
    init_dataset_catalog()


def serialize(dataset):
    return {
        "id": dataset.id,
        "code": dataset.code,
        "name": dataset.name,
        "description": dataset.description,
        "source_type": dataset.source.source_type,
        "source_location": dataset.source.location,
        "record_count": dataset.metrics.record_count,
        "active": dataset.active,
        "created_at": (
            dataset.created_at.isoformat()
            if dataset.created_at
            else None
        ),
        "updated_at": (
            dataset.updated_at.isoformat()
            if dataset.updated_at
            else None
        ),
    }


@router.post(
    "",
    response_model=DatasetResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_dataset(
    payload: DatasetCreateDTO,
    db: Session = Depends(get_db),
):
    repository = SqlDatasetRepository(db)

    use_case = CreateDataset(repository)

    try:
        dataset = use_case.execute(
            code=payload.code,
            name=payload.name,
            description=payload.description,
            source_type=payload.source_type,
            source_location=payload.source_location,
            record_count=payload.record_count,
            active=payload.active,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        db.rollback()

        if "UNIQUE constraint failed" in str(exc):
            raise HTTPException(
                status_code=409,
                detail=f"El código ya existe: {payload.code}",
            )

        raise

    return serialize(dataset)


@router.get(
    "",
    response_model=list[DatasetResponseDTO],
)
def list_datasets(
    db: Session = Depends(get_db),
):
    repository = SqlDatasetRepository(db)

    use_case = ListDatasets(repository)

    return [
        serialize(dataset)
        for dataset in use_case.execute()
    ]


@router.get(
    "/{dataset_id}",
    response_model=DatasetResponseDTO,
)
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    repository = SqlDatasetRepository(db)

    use_case = GetDataset(repository)

    dataset = use_case.execute(dataset_id)

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset no encontrado",
        )

    return serialize(dataset)


@router.put(
    "/{dataset_id}",
    response_model=DatasetResponseDTO,
)
def update_dataset(
    dataset_id: int,
    payload: DatasetUpdateDTO,
    db: Session = Depends(get_db),
):
    repository = SqlDatasetRepository(db)

    current = GetDataset(repository).execute(dataset_id)

    if current is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset no encontrado",
        )

    use_case = UpdateDataset(repository)

    try:
        dataset = use_case.execute(
            dataset_id=dataset_id,
            current=current,
            name=payload.name,
            description=payload.description,
            source_type=payload.source_type,
            source_location=payload.source_location,
            record_count=payload.record_count,
            active=payload.active,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return serialize(dataset)


@router.delete(
    "/{dataset_id}",
)
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    repository = SqlDatasetRepository(db)

    use_case = DeleteDataset(repository)

    deleted = use_case.execute(dataset_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dataset no encontrado",
        )

    return {
        "deleted": True,
        "id": dataset_id,
    }
