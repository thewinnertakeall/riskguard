from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DatasetCatalogModel(Base):
    """
    Persistencia del catálogo.

    IMPORTANTE:
    Esta tabla es independiente de external_risk_data.
    """

    __tablename__ = "dataset_catalog"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    source_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    source_location: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    record_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
