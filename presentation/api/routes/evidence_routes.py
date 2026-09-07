from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EvidenceCreate, EvidenceUpdate, EvidenceResponse

from application.use_cases.create_evidence import create_evidence
from application.use_cases.list_evidence import list_evidence
from application.use_cases.get_evidence import get_evidence
from application.use_cases.update_evidence import update_evidence
from application.use_cases.delete_evidence import delete_evidence


router = APIRouter(
    prefix="/api/v2/evidence",
    tags=["Evidence"]
)


@router.get("", response_model=list[EvidenceResponse])
def list_evidence_endpoint(
    status: str | None = None,
    risk_id: int | None = None,
    iso_control_id: int | None = None,
    db: Session = Depends(get_db),
):
    return list_evidence(
        db=db,
        status=status,
        risk_id=risk_id,
        iso_control_id=iso_control_id,
    )


@router.get("/{code}", response_model=EvidenceResponse)
def get_evidence_endpoint(
    code: str,
    db: Session = Depends(get_db),
):
    evidence = get_evidence(
        db=db,
        code=code,
    )

    if evidence is None:
        raise HTTPException(
            status_code=404,
            detail=f"Evidence {code} not found"
        )

    return evidence


@router.post(
    "",
    response_model=EvidenceResponse,
    status_code=201,
)
def create_evidence_endpoint(
    data: EvidenceCreate,
    db: Session = Depends(get_db),
):
    evidence, status = create_evidence(
        db=db,
        **data.model_dump(),
    )

    if status == "already_exists":
        raise HTTPException(
            status_code=409,
            detail=f"Evidence {data.code} already exists"
        )

    if status == "iso_control_not_found":
        raise HTTPException(
            status_code=404,
            detail=f"ISO control {data.iso_control_id} not found"
        )

    if status == "risk_not_found":
        raise HTTPException(
            status_code=404,
            detail=f"Risk {data.risk_id} not found"
        )

    return evidence


@router.put(
    "/{code}",
    response_model=EvidenceResponse,
)
def update_evidence_endpoint(
    code: str,
    data: EvidenceUpdate,
    db: Session = Depends(get_db),
):
    payload = data.model_dump(exclude_unset=True)

    payload.pop("code", None)

    evidence, status = update_evidence(
        db=db,
        code=code,
        **payload,
    )

    if status == "evidence_not_found":
        raise HTTPException(
            status_code=404,
            detail=f"Evidence {code} not found"
        )

    if status == "iso_control_not_found":
        raise HTTPException(
            status_code=404,
            detail=f"ISO control {data.iso_control_id} not found"
        )

    if status == "risk_not_found":
        raise HTTPException(
            status_code=404,
            detail=f"Risk {data.risk_id} not found"
        )

    return evidence


@router.delete("/{code}")
def delete_evidence_endpoint(
    code: str,
    db: Session = Depends(get_db),
):
    evidence, status = delete_evidence(
        db=db,
        code=code,
    )

    if status == "evidence_not_found":
        raise HTTPException(
            status_code=404,
            detail=f"Evidence {code} not found"
        )

    return {
        "message": "Evidence deleted",
        "code": code,
    }
