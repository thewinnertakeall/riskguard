from sqlalchemy.orm import Session

from application.services.evidence_service import EvidenceService


def create_evidence(
    db: Session,
    **data
):
    return EvidenceService.create(
        db=db,
        **data
    )
