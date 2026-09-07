from sqlalchemy.orm import Session

from application.services.evidence_service import EvidenceService


def list_evidence(
    db: Session,
    status: str | None = None,
    risk_id: int | None = None,
    iso_control_id: int | None = None,
):
    return EvidenceService.list_evidence(
        db=db,
        status=status,
        risk_id=risk_id,
        iso_control_id=iso_control_id,
    )
