from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models
from .schemas import (
    AreaCreate,
    CauseCreate,
    CauseUpdate,
    ControlCreate,
    ControlUpdate,
    IncidentCreate,
    IncidentUpdate,
    LocationCreate,
    ProcessCreate,
    RiskCreate,
    RiskUpdate,
)


# ============================================================
# RISK
# ============================================================

# DUPLICATE_CODE_HANDLING
def create_risk(db: Session, risk: RiskCreate):
    data = risk.model_dump()

    if db.query(models.Risk).filter(
        models.Risk.code == data["code"]
    ).first():
        raise ValueError(f"Risk code '{data['code']}' already exists")

    data["risk_score"] = data["probability"] * data["impact"]

    if data["risk_score"] <= 4:
        data["risk_level"] = "Low"
    elif data["risk_score"] <= 9:
        data["risk_level"] = "Medium"
    elif data["risk_score"] <= 16:
        data["risk_level"] = "High"
    else:
        data["risk_level"] = "Critical"

    db_risk = models.Risk(**data)

    try:
        db.add(db_risk)
        db.commit()
        db.refresh(db_risk)
    except IntegrityError as exc:
        db.rollback()
        if db.query(models.Risk).filter(
            models.Risk.code == data["code"]
        ).first():
            raise ValueError(
                f"Risk code '{data['code']}' already exists"
            ) from exc
        raise

    return db_risk


def get_risks(db: Session):
    return db.query(models.Risk).all()


def get_risk(db: Session, risk_id: int):
    return (
        db.query(models.Risk)
        .filter(models.Risk.id == risk_id)
        .first()
    )


def update_risk(
    db: Session,
    risk_id: int,
    risk: RiskUpdate
):
    db_risk = get_risk(db, risk_id)

    if not db_risk:
        return None

    data = risk.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_risk, key, value)

    if (
        "probability" in data
        or "impact" in data
    ):
        db_risk.risk_score = (
            db_risk.probability *
            db_risk.impact
        )

        if db_risk.risk_score <= 4:
            db_risk.risk_level = "Low"
        elif db_risk.risk_score <= 9:
            db_risk.risk_level = "Medium"
        elif db_risk.risk_score <= 16:
            db_risk.risk_level = "High"
        else:
            db_risk.risk_level = "Critical"

    db.commit()
    db.refresh(db_risk)

    return db_risk


def delete_risk(db: Session, risk_id: int):
    db_risk = get_risk(db, risk_id)

    if not db_risk:
        return None

    db.delete(db_risk)
    db.commit()

    return db_risk


# ============================================================
# CAUSE
# ============================================================

def create_cause(db: Session, cause: CauseCreate):
    db_cause = models.Cause(
        **cause.model_dump()
    )

    db.add(db_cause)
    db.commit()
    db.refresh(db_cause)

    return db_cause


def get_causes(db: Session):
    return db.query(models.Cause).all()


def get_cause(db: Session, cause_id: int):
    return (
        db.query(models.Cause)
        .filter(models.Cause.id == cause_id)
        .first()
    )


def update_cause(
    db: Session,
    cause_id: int,
    cause: CauseUpdate
):
    db_cause = get_cause(db, cause_id)

    if not db_cause:
        return None

    data = cause.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(db_cause, key, value)

    db.commit()
    db.refresh(db_cause)

    return db_cause


def delete_cause(
    db: Session,
    cause_id: int
):
    db_cause = get_cause(db, cause_id)

    if not db_cause:
        return None

    db.delete(db_cause)
    db.commit()

    return db_cause


# ============================================================
# CONTROL
# ============================================================

def create_control(
    db: Session,
    control: ControlCreate
):
    db_control = models.Control(
        **control.model_dump()
    )

    db.add(db_control)
    db.commit()
    db.refresh(db_control)

    return db_control


def get_controls(db: Session):
    return db.query(models.Control).all()


def get_control(
    db: Session,
    control_id: int
):
    return (
        db.query(models.Control)
        .filter(models.Control.id == control_id)
        .first()
    )


def update_control(
    db: Session,
    control_id: int,
    control: ControlUpdate
):
    db_control = get_control(
        db,
        control_id
    )

    if not db_control:
        return None

    data = control.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(db_control, key, value)

    db.commit()
    db.refresh(db_control)

    return db_control


def delete_control(
    db: Session,
    control_id: int
):
    db_control = get_control(
        db,
        control_id
    )

    if not db_control:
        return None

    db.delete(db_control)
    db.commit()

    return db_control


# ============================================================
# INCIDENT
# ============================================================

# DUPLICATE_CODE_HANDLING
def create_incident(
    db: Session,
    incident: IncidentCreate
):
    data = incident.model_dump()

    if db.query(models.Incident).filter(
        models.Incident.code == data["code"]
    ).first():
        raise ValueError(
            f"Incident code '{data['code']}' already exists"
        )

    db_incident = models.Incident(**data)

    try:
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
    except IntegrityError as exc:
        db.rollback()
        if db.query(models.Incident).filter(
            models.Incident.code == data["code"]
        ).first():
            raise ValueError(
                f"Incident code '{data['code']}' already exists"
            ) from exc
        raise

    return db_incident


def get_incidents(db: Session):
    return db.query(models.Incident).all()


def get_incident(
    db: Session,
    incident_id: int
):
    return (
        db.query(models.Incident)
        .filter(
            models.Incident.id == incident_id
        )
        .first()
    )


def update_incident(
    db: Session,
    incident_id: int,
    incident: IncidentUpdate
):
    db_incident = get_incident(
        db,
        incident_id
    )

    if not db_incident:
        return None

    data = incident.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(db_incident, key, value)

    db.commit()
    db.refresh(db_incident)

    return db_incident


def delete_incident(
    db: Session,
    incident_id: int
):
    db_incident = get_incident(
        db,
        incident_id
    )

    if not db_incident:
        return None

    db.delete(db_incident)
    db.commit()

    return db_incident


# ============================================================
# PROCESS
# ============================================================

def create_process(
    db: Session,
    process: ProcessCreate
):
    db_process = models.Process(
        **process.model_dump()
    )

    db.add(db_process)
    db.commit()
    db.refresh(db_process)

    return db_process


def get_processes(db: Session):
    return db.query(models.Process).all()


# ============================================================
# AREA
# ============================================================

def create_area(
    db: Session,
    area: AreaCreate
):
    db_area = models.Area(
        **area.model_dump()
    )

    db.add(db_area)
    db.commit()
    db.refresh(db_area)

    return db_area


def get_areas(db: Session):
    return db.query(models.Area).all()


# ============================================================
# LOCATION
# ============================================================

def create_location(
    db: Session,
    location: LocationCreate
):
    db_location = models.Location(
        **location.model_dump()
    )

    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    return db_location


def get_locations(db: Session):
    return db.query(models.Location).all()


# ============================================================
# RELATIONSHIPS
# ============================================================

def assign_cause_to_risk(
    db: Session,
    risk_id: int,
    cause_id: int
):
    risk = get_risk(db, risk_id)
    cause = get_cause(db, cause_id)

    if not risk or not cause:
        return None

    if cause not in risk.causes:
        risk.causes.append(cause)

    db.commit()
    db.refresh(risk)

    return risk


def assign_control_to_risk(
    db: Session,
    risk_id: int,
    control_id: int
):
    risk = get_risk(db, risk_id)
    control = get_control(db, control_id)

    if not risk or not control:
        return None

    if control not in risk.controls:
        risk.controls.append(control)

    db.commit()
    db.refresh(risk)

    return risk


def assign_incident_to_risk(
    db: Session,
    risk_id: int,
    incident_id: int
):
    risk = get_risk(db, risk_id)
    incident = get_incident(db, incident_id)

    if risk is None or incident is None:
        return None

    if incident in risk.incidents:
        return risk

    try:
        risk.incidents.append(incident)
        db.commit()
        db.refresh(risk)
    except IntegrityError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise

    return risk
