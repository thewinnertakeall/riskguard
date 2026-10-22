from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class ISOControl(Base):
    __tablename__ = "iso_controls"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String(30),
        unique=True,
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    category = Column(
        String(100)
    )

    implementation_status = Column(
        String(50),
        default="Not Implemented",
        nullable=False
    )

    effectiveness = Column(
        Float,
        default=0.0,
        nullable=False
    )

    applicable = Column(
        Boolean,
        default=True,
        nullable=False
    )

    evidence_required = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )

    updated_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    risk_links = relationship(
        "RiskISOControl",
        back_populates="iso_control",
        cascade="all, delete-orphan"
    )
