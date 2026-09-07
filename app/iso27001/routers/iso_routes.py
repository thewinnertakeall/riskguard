from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.iso27001.services.compliance import (
    get_controls,
    get_control_by_code,
    calculate_compliance,
)
from app.models.iso_control import ISOControl


router = APIRouter(
    prefix="/api/iso27001",
    tags=["ISO 27001"],
)


class ISOControlUpdate(BaseModel):
    implementation_status: str | None = None
    effectiveness: float | None = None
    applicable: bool | None = None
    evidence_required: bool | None = None


@router.get("/status")
def iso_status():
    return {
        "standard": "ISO/IEC 27001:2022",
        "system": "RiskGuard",
        "status": "operational",
        "storage": "SQLite",
        "message": (
            "RiskGuard ISO 27001 compliance "
            "module operational"
        ),
    }


@router.get("/controls")
def iso_controls(db: Session = Depends(get_db)):
    return get_controls(db)


@router.get("/controls/{code}")
def iso_control(
    code: str,
    db: Session = Depends(get_db),
):
    control = get_control_by_code(db, code)

    if not control:
        raise HTTPException(
            status_code=404,
            detail=f"ISO control {code} not found",
        )

    return control


@router.patch("/controls/{code}")
def update_iso_control(
    code: str,
    data: ISOControlUpdate,
    db: Session = Depends(get_db),
):
    control = get_control_by_code(db, code)

    if not control:
        raise HTTPException(
            status_code=404,
            detail=f"ISO control {code} not found",
        )

    if data.implementation_status is not None:
        allowed_statuses = {
            "Not Implemented",
            "Partial",
            "Implemented",
        }

        if data.implementation_status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=(
                    "implementation_status must be one of: "
                    "Not Implemented, Partial, Implemented"
                ),
            )

        control.implementation_status = data.implementation_status

    if data.effectiveness is not None:
        if not 0 <= data.effectiveness <= 100:
            raise HTTPException(
                status_code=400,
                detail="effectiveness must be between 0 and 100",
            )

        control.effectiveness = data.effectiveness

    if data.applicable is not None:
        control.applicable = data.applicable

    if data.evidence_required is not None:
        control.evidence_required = data.evidence_required

    db.commit()
    db.refresh(control)

    return control


@router.get("/compliance")
def iso_compliance(db: Session = Depends(get_db)):
    return calculate_compliance(db)


@router.get("/soa")
def statement_of_applicability(
    db: Session = Depends(get_db),
):
    controls = get_controls(db)

    return {
        "standard": "ISO/IEC 27001:2022",
        "document": "Statement of Applicability",
        "controls": controls,
    }
