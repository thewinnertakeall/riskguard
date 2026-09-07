from sqlalchemy.orm import Session

from application.services.risk_service import RiskService
from infrastructure.database.repositories.sql_risk_repository import (
    SQLRiskRepository,
)


class ApplicationContainer:

    def __init__(self, db: Session):
        self.db = db

    def risk_repository(self) -> SQLRiskRepository:
        return SQLRiskRepository(self.db)

    def risk_service(self) -> RiskService:
        return RiskService(
            repository=self.risk_repository()
        )
