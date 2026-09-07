from sqlalchemy.orm import Session

from app.models import Evidence, Risk, ISOControl


class EvidenceService:

    @staticmethod
    def list_evidence(
        db: Session,
        status: str | None = None,
        risk_id: int | None = None,
        iso_control_id: int | None = None,
    ):
        query = db.query(Evidence)

        if status:
            query = query.filter(Evidence.status == status)

        if risk_id is not None:
            query = query.filter(Evidence.risk_id == risk_id)

        if iso_control_id is not None:
            query = query.filter(
                Evidence.iso_control_id == iso_control_id
            )

        return (
            query
            .order_by(Evidence.id.desc())
            .all()
        )

    @staticmethod
    def get_by_code(
        db: Session,
        code: str
    ):
        return (
            db.query(Evidence)
            .filter(Evidence.code == code)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        code: str,
        title: str,
        description: str | None = None,
        evidence_type: str | None = None,
        file_path: str | None = None,
        source: str | None = None,
        hash_sha256: str | None = None,
        status: str = "Active",
        collected_at=None,
        owner: str | None = None,
        iso_control_id: int | None = None,
        risk_id: int | None = None,
        event_id: int | None = None,
    ):
        existing = (
            db.query(Evidence)
            .filter(Evidence.code == code)
            .first()
        )

        if existing:
            return existing, "already_exists"

        if iso_control_id is not None:
            control = (
                db.query(ISOControl)
                .filter(ISOControl.id == iso_control_id)
                .first()
            )

            if not control:
                return None, "iso_control_not_found"

        if risk_id is not None:
            risk = (
                db.query(Risk)
                .filter(Risk.id == risk_id)
                .first()
            )

            if not risk:
                return None, "risk_not_found"

        evidence = Evidence(
            code=code,
            title=title,
            description=description,
            evidence_type=evidence_type,
            file_path=file_path,
            source=source,
            hash_sha256=hash_sha256,
            status=status,
            collected_at=collected_at,
            owner=owner,
            iso_control_id=iso_control_id,
            risk_id=risk_id,
            event_id=event_id,
        )

        db.add(evidence)
        db.commit()
        db.refresh(evidence)

        return evidence, "created"

    @staticmethod
    def update(
        db: Session,
        code: str,
        title: str | None = None,
        description: str | None = None,
        evidence_type: str | None = None,
        file_path: str | None = None,
        source: str | None = None,
        hash_sha256: str | None = None,
        status: str | None = None,
        collected_at=None,
        owner: str | None = None,
        iso_control_id: int | None = None,
        risk_id: int | None = None,
        event_id: int | None = None,
    ):
        evidence = (
            db.query(Evidence)
            .filter(Evidence.code == code)
            .first()
        )

        if not evidence:
            return None, "evidence_not_found"

        if iso_control_id is not None:
            control = (
                db.query(ISOControl)
                .filter(ISOControl.id == iso_control_id)
                .first()
            )

            if not control:
                return None, "iso_control_not_found"

        if risk_id is not None:
            risk = (
                db.query(Risk)
                .filter(Risk.id == risk_id)
                .first()
            )

            if not risk:
                return None, "risk_not_found"

        fields = {
            "title": title,
            "description": description,
            "evidence_type": evidence_type,
            "file_path": file_path,
            "source": source,
            "hash_sha256": hash_sha256,
            "status": status,
            "collected_at": collected_at,
            "owner": owner,
            "iso_control_id": iso_control_id,
            "risk_id": risk_id,
            "event_id": event_id,
        }

        for field, value in fields.items():
            if value is not None:
                setattr(evidence, field, value)

        db.commit()
        db.refresh(evidence)

        return evidence, "updated"

    @staticmethod
    def delete(
        db: Session,
        code: str
    ):
        evidence = (
            db.query(Evidence)
            .filter(Evidence.code == code)
            .first()
        )

        if not evidence:
            return None, "evidence_not_found"

        db.delete(evidence)
        db.commit()

        return evidence, "deleted"
