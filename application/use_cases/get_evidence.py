from sqlalchemy.orm import Session

from application.services.evidence_service import EvidenceService


def get_evidence(
    db: Session,
    code: str
):
    return EvidenceService.get_by_code(
        db=db,
        code=code
    )
