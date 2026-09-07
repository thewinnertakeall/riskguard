from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from infrastructure.container.container import ApplicationContainer
from application.services.risk_service import RiskService


def get_container(
    db: Session = Depends(get_db),
) -> ApplicationContainer:

    return ApplicationContainer(db)


def get_risk_service(
    container: ApplicationContainer = Depends(get_container),
) -> RiskService:

    return container.risk_service()
