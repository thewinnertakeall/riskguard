from sqlalchemy.orm import Session

from application.services.evidence_service import EvidenceService


def delete_evidence(
    db: Session,
    code: str
):
    return EvidenceService.delete(
        db=db,
        code=code
    )
