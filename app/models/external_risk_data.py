from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class ExternalRiskData(Base):
    """
    External occupational risk statistics imported from
    official public open-data sources.

    Source dataset:
    Datos Abiertos Colombia - Estadísticas Riesgos Laborales Positiva 2026
    """

    __tablename__ = "external_risk_data"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ---------------------------------------------------------
    # DATA SOURCE
    # ---------------------------------------------------------

    source = Column(
        String(150),
        nullable=False
    )

    source_url = Column(
        String(500),
        nullable=False
    )

    # ---------------------------------------------------------
    # REPORT PERIOD
    # ---------------------------------------------------------

    report_year = Column(
        Integer,
        nullable=False
    )

    report_month = Column(
        Integer,
        nullable=True
    )

    # ---------------------------------------------------------
    # GEOGRAPHIC / ORGANIZATIONAL INFORMATION
    # ---------------------------------------------------------

    department = Column(
        String(150),
        nullable=True
    )

    municipality = Column(
        String(150),
        nullable=True
    )

    arl_code = Column(
        String(50),
        nullable=True
    )

    # ---------------------------------------------------------
    # ECONOMIC ACTIVITY
    # ---------------------------------------------------------

    economic_activity_code = Column(
        String(100),
        nullable=True
    )

    # ---------------------------------------------------------
    # AFFILIATION / POPULATION
    # ---------------------------------------------------------

    dependent_workers = Column(
        Integer,
        nullable=True
    )

    independent_workers = Column(
        Integer,
        nullable=True
    )

    # ---------------------------------------------------------
    # OCCUPATIONAL ACCIDENTS
    # ---------------------------------------------------------

    reported_accidents = Column(
        Integer,
        nullable=True
    )

    # ---------------------------------------------------------
    # WORK-RELATED DEATHS
    # ---------------------------------------------------------

    reported_work_deaths = Column(
        Integer,
        nullable=True
    )

    # ---------------------------------------------------------
    # INVALIDITY / PENSION VARIABLES
    # ---------------------------------------------------------

    disability_pension_accident = Column(
        Integer,
        nullable=True
    )

    disability_pension_occupational_disease = Column(
        Integer,
        nullable=True
    )

    # ---------------------------------------------------------
    # PERMANENT PARTIAL DISABILITY
    # ---------------------------------------------------------

    permanent_partial_disability_accident = Column(
        Integer,
        nullable=True
    )

    permanent_partial_disability_occupational_disease = Column(
        Integer,
        nullable=True
    )

    # ---------------------------------------------------------
    # AUDIT / TRACEABILITY
    # ---------------------------------------------------------

    imported_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False
    )
