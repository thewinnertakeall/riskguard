"""
RF-06
LOAD: persiste registros transformados en SQLite.
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


NATURAL_KEY_FIELDS = (
    "source",
    "report_year",
    "report_month",
    "department",
    "municipality",
    "arl_code",
    "economic_activity_code",
)


def build_natural_key(record):
    """
    Construye la clave lógica de un registro externo.
    """

    return tuple(
        record.get(field)
        for field in NATURAL_KEY_FIELDS
    )


def load_records(records):
    """
    Inserta únicamente registros que no existan.

    No realiza HTTP.
    No transforma datos.
    No genera evidencia.
    """

    db = SessionLocal()

    inserted = 0
    duplicates = 0

    try:
        existing_keys = {
            build_natural_key(
                {
                    field: getattr(row, field)
                    for field in NATURAL_KEY_FIELDS
                }
            )
            for row in db.query(ExternalRiskData).all()
        }

        for record in records:
            natural_key = build_natural_key(record)

            if natural_key in existing_keys:
                duplicates += 1
                continue

            db.add(
                ExternalRiskData(**record)
            )

            existing_keys.add(natural_key)
            inserted += 1

        db.commit()

        return {
            "inserted": inserted,
            "duplicates": duplicates,
            "total": len(records),
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
