from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# RISK
# ============================================================

class RiskBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None

    process_id: Optional[int] = None
    area_id: Optional[int] = None
    location_id: Optional[int] = None

    category: Optional[str] = None

    probability: int = Field(default=1, ge=1, le=5)
    impact: int = Field(default=1, ge=1, le=5)

    risk_score: int = Field(default=1, ge=1, le=25)

    risk_level: str = "Low"
    status: str = "Active"


class RiskCreate(RiskBase):
    pass


class RiskUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    process_id: Optional[int] = None
    area_id: Optional[int] = None
    location_id: Optional[int] = None

    category: Optional[str] = None

    probability: Optional[int] = Field(
        default=None,
        ge=1,
        le=5
    )

    impact: Optional[int] = Field(
        default=None,
        ge=1,
        le=5
    )

    risk_score: Optional[int] = Field(
        default=None,
        ge=1,
        le=25
    )

    risk_level: Optional[str] = None
    status: Optional[str] = None


class RiskResponse(RiskBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# CAUSE
# ============================================================

class CauseBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    cause_type: Optional[str] = None
    status: str = "Active"


class CauseCreate(CauseBase):
    pass


class CauseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    cause_type: Optional[str] = None
    status: Optional[str] = None


class CauseResponse(CauseBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# CONTROL
# ============================================================

class ControlBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None

    control_type: Optional[str] = None
    hierarchy_level: Optional[str] = None

    effectiveness: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    status: str = "Active"


class ControlCreate(ControlBase):
    pass


class ControlUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    control_type: Optional[str] = None
    hierarchy_level: Optional[str] = None

    effectiveness: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    status: Optional[str] = None


class ControlResponse(ControlBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# INCIDENT
# ============================================================

class IncidentBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

    incident_date: Optional[date] = None

    incident_type: Optional[str] = None
    severity: Optional[str] = None

    location_id: Optional[int] = None

    status: str = "Open"


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    incident_date: Optional[date] = None

    incident_type: Optional[str] = None
    severity: Optional[str] = None

    location_id: Optional[int] = None

    status: Optional[str] = None


class IncidentResponse(IncidentBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# PROCESS
# ============================================================

class ProcessBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None


class ProcessCreate(ProcessBase):
    pass


class ProcessResponse(ProcessBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# AREA
# ============================================================

class AreaBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None


class AreaCreate(AreaBase):
    pass


class AreaResponse(AreaBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# LOCATION
# ============================================================

class LocationBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# EVIDENCE
# ============================================================

class EvidenceBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)

    description: Optional[str] = None
    evidence_type: Optional[str] = None
    file_path: Optional[str] = None
    source: Optional[str] = None

    hash_sha256: Optional[str] = Field(
        default=None,
        min_length=64,
        max_length=64
    )

    status: str = "Active"

    collected_at: Optional[date] = None
    owner: Optional[str] = None

    iso_control_id: Optional[int] = None
    risk_id: Optional[int] = None
    event_id: Optional[int] = None


class EvidenceCreate(EvidenceBase):
    pass


class EvidenceUpdate(BaseModel):
    code: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: Optional[str] = None
    evidence_type: Optional[str] = None
    file_path: Optional[str] = None
    source: Optional[str] = None

    hash_sha256: Optional[str] = Field(
        default=None,
        min_length=64,
        max_length=64
    )

    status: Optional[str] = None
    collected_at: Optional[date] = None
    owner: Optional[str] = None

    iso_control_id: Optional[int] = None
    risk_id: Optional[int] = None
    event_id: Optional[int] = None


class EvidenceResponse(EvidenceBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
