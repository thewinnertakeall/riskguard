from sqlalchemy.orm import Session

from app.models.iso_control import ISOControl


def get_controls(db: Session):
    """
    Obtiene los controles ISO desde SQLite.
    """

    return (
        db.query(ISOControl)
        .order_by(ISOControl.code)
        .all()
    )


def get_control_by_code(
    db: Session,
    code: str
):
    """
    Obtiene un control específico por código.
    """

    return (
        db.query(ISOControl)
        .filter(ISOControl.code == code)
        .first()
    )


def calculate_compliance(db: Session):
    """
    Calcula un indicador interno de avance del SGSI.

    Implemented = 100%
    Partial = 50%
    Not Implemented = 0%

    Este porcentaje es una métrica interna de RiskGuard,
    no un porcentaje oficial de certificación ISO 27001.
    """

    controls = (
        db.query(ISOControl)
        .filter(ISOControl.applicable == True)
        .all()
    )

    total = len(controls)

    implemented = sum(
        1
        for control in controls
        if control.implementation_status.lower()
        == "implemented"
    )

    partial = sum(
        1
        for control in controls
        if control.implementation_status.lower()
        == "partial"
    )

    pending = total - implemented - partial

    percentage = (
        round(
            (
                implemented
                + partial * 0.5
            )
            / total
            * 100,
            2
        )
        if total
        else 0
    )

    return {
        "standard": "ISO/IEC 27001:2022",
        "total_controls": total,
        "implemented": implemented,
        "partial": partial,
        "pending": pending,
        "compliance_percentage": percentage
    }
