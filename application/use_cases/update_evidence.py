from sqlalchemy.orm import Session

from application.services.evidence_service import EvidenceService


def update_evidence(
    db: Session,
    code: str,
    **data
):
    return EvidenceService.update(
        db=db,
        code=code,
        **data
    )
