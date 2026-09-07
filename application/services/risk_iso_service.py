from sqlalchemy.orm import Session

from app.models import Risk, ISOControl, RiskISOControl


class RiskISOService:

    @staticmethod
    def get_links(
        db: Session,
        risk_code: str
    ):
        risk = (
            db.query(Risk)
            .filter(Risk.code == risk_code)
            .first()
        )

        if not risk:
            return None, []

        links = (
            db.query(RiskISOControl)
            .filter(RiskISOControl.risk_id == risk.id)
            .all()
        )

        return risk, links

    @staticmethod
    def create_link(
        db: Session,
        risk_code: str,
        iso_control_code: str,
        treatment_status: str = "Planned",
        notes: str | None = None,
    ):
        risk = (
            db.query(Risk)
            .filter(Risk.code == risk_code)
            .first()
        )

        if not risk:
            return None, "risk_not_found"

        control = (
            db.query(ISOControl)
            .filter(ISOControl.code == iso_control_code)
            .first()
        )

        if not control:
            return None, "iso_control_not_found"

        existing = (
            db.query(RiskISOControl)
            .filter(
                RiskISOControl.risk_id == risk.id,
                RiskISOControl.iso_control_id == control.id,
            )
            .first()
        )

        if existing:
            return existing, "already_exists"

        link = RiskISOControl(
            risk_id=risk.id,
            iso_control_id=control.id,
            treatment_status=treatment_status,
            notes=notes,
        )

        db.add(link)
        db.commit()
        db.refresh(link)

        return link, "created"

    @staticmethod
    def delete_link(
        db: Session,
        risk_code: str,
        iso_control_code: str,
    ):
        risk = (
            db.query(Risk)
            .filter(Risk.code == risk_code)
            .first()
        )

        if not risk:
            return None, "risk_not_found"

        control = (
            db.query(ISOControl)
            .filter(ISOControl.code == iso_control_code)
            .first()
        )

        if not control:
            return None, "iso_control_not_found"

        link = (
            db.query(RiskISOControl)
            .filter(
                RiskISOControl.risk_id == risk.id,
                RiskISOControl.iso_control_id == control.id,
            )
            .first()
        )

        if not link:
            return None, "link_not_found"

        db.delete(link)
        db.commit()

        return link, "deleted"

    @staticmethod
    def update_link(
        db: Session,
        risk_code: str,
        iso_control_code: str,
        treatment_status: str = "Planned",
        notes: str | None = None,
    ):
        risk = (
            db.query(Risk)
            .filter(Risk.code == risk_code)
            .first()
        )

        if not risk:
            return None, "risk_not_found"

        control = (
            db.query(ISOControl)
            .filter(ISOControl.code == iso_control_code)
            .first()
        )

        if not control:
            return None, "iso_control_not_found"

        link = (
            db.query(RiskISOControl)
            .filter(
                RiskISOControl.risk_id == risk.id,
                RiskISOControl.iso_control_id == control.id,
            )
            .first()
        )

        if not link:
            return None, "link_not_found"

        link.treatment_status = treatment_status
        link.notes = notes

        db.commit()
        db.refresh(link)

        return link, "updated"
