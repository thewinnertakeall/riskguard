"""
RF-07
Repository de datos públicos de riesgos laborales.

Responsabilidad:
    Leer external_risk_data desde SQLite.

Este módulo NO:
    - realiza HTTP
    - transforma datos
    - calcula indicadores
    - expone endpoints
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.external_risk_data import ExternalRiskData
from scripts.rf06.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class PublicRiskRepository:
    """
    Acceso de lectura a los datos públicos
    previamente cargados por RF-06.
    """

    def get_all(self):
        db = SessionLocal()

        try:
            return (
                db.query(ExternalRiskData)
                .all()
            )

        finally:
            db.close()

    def count(self):
        db = SessionLocal()

        try:
            return (
                db.query(ExternalRiskData)
                .count()
            )

        finally:
            db.close()
