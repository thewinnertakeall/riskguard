#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "=============================================="
echo "RISKGUARD - PHASE B"
echo "Repository + Service + Use Case + DTO + DI"
echo "=============================================="

cd "$PROJECT_ROOT"

mkdir -p infrastructure/database/repositories
mkdir -p infrastructure/container
mkdir -p application/use_cases
mkdir -p presentation/api/controllers
mkdir -p presentation/api/routes
mkdir -p presentation/schemas

touch infrastructure/container/__init__.py

# ------------------------------------------------
# 1. DOMAIN REPOSITORY INTERFACE
# ------------------------------------------------

cat << 'PY' > domain/interfaces/risk_repository.py
from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.risk import Risk


class RiskRepository(ABC):

    @abstractmethod
    def find_by_id(self, risk_id: int) -> Optional[Risk]:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Risk]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Risk]:
        raise NotImplementedError

    @abstractmethod
    def save(self, risk: Risk) -> Risk:
        raise NotImplementedError
PY

# ------------------------------------------------
# 2. SQL REPOSITORY IMPLEMENTATION
# ------------------------------------------------

cat << 'PY' > infrastructure/database/repositories/sql_risk_repository.py
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Risk as RiskModel

from domain.entities.risk import Risk
from domain.interfaces.risk_repository import RiskRepository


class SQLRiskRepository(RiskRepository):

    def __init__(self, session: Session):
        self.session = session

    def _to_entity(self, model: RiskModel) -> Risk:
        return Risk(
            code=model.code,
            name=model.name,
            probability=model.probability,
            impact=model.impact,
            description=model.description,
            category=model.category,
            status=model.status,
        )

    def find_by_id(self, risk_id: int) -> Optional[Risk]:
        model = (
            self.session
            .query(RiskModel)
            .filter(RiskModel.id == risk_id)
            .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def find_by_code(self, code: str) -> Optional[Risk]:
        model = (
            self.session
            .query(RiskModel)
            .filter(RiskModel.code == code)
            .first()
        )

        if model is None:
            return None

        return self._to_entity(model)

    def find_all(self) -> list[Risk]:
        models = (
            self.session
            .query(RiskModel)
            .order_by(RiskModel.id)
            .all()
        )

        return [self._to_entity(model) for model in models]

    def save(self, risk: Risk) -> Risk:
        model = (
            self.session
            .query(RiskModel)
            .filter(RiskModel.code == risk.code)
            .first()
        )

        if model is None:
            model = RiskModel(
                code=risk.code,
                name=risk.name,
                description=risk.description,
                category=risk.category,
                probability=risk.probability,
                impact=risk.impact,
                risk_score=risk.calculate_score(),
                risk_level=risk.classify(),
                status=risk.status,
            )

            self.session.add(model)

        else:
            model.name = risk.name
            model.description = risk.description
            model.category = risk.category
            model.probability = risk.probability
            model.impact = risk.impact
            model.risk_score = risk.calculate_score()
            model.risk_level = risk.classify()
            model.status = risk.status

        self.session.commit()
        self.session.refresh(model)

        return self._to_entity(model)
PY

# ------------------------------------------------
# 3. RISK DTO
# ------------------------------------------------

cat << 'PY' > application/dto/risk_dto.py
from dataclasses import dataclass


@dataclass
class RiskDTO:
    code: str
    name: str
    description: str | None
    category: str | None
    probability: int
    impact: int
    risk_score: int
    risk_level: str
    status: str | None

    @classmethod
    def from_entity(cls, risk):
        return cls(
            code=risk.code,
            name=risk.name,
            description=risk.description,
            category=risk.category,
            probability=risk.probability,
            impact=risk.impact,
            risk_score=risk.calculate_score(),
            risk_level=risk.classify(),
            status=risk.status,
        )
PY

# ------------------------------------------------
# 4. RISK SERVICE
# ------------------------------------------------

cat << 'PY' > application/services/risk_service.py
from application.dto.risk_dto import RiskDTO
from domain.entities.risk import Risk
from domain.interfaces.risk_repository import RiskRepository


class RiskService:

    def __init__(self, repository: RiskRepository):
        self.repository = repository

    def get_risk(self, code: str) -> RiskDTO | None:
        risk = self.repository.find_by_code(code)

        if risk is None:
            return None

        return RiskDTO.from_entity(risk)

    def get_all_risks(self) -> list[RiskDTO]:
        risks = self.repository.find_all()

        return [
            RiskDTO.from_entity(risk)
            for risk in risks
        ]

    def create_risk(
        self,
        code: str,
        name: str,
        probability: int,
        impact: int,
        description: str | None = None,
        category: str | None = None,
        status: str | None = "active",
    ) -> RiskDTO:

        risk = Risk(
            code=code,
            name=name,
            probability=probability,
            impact=impact,
            description=description,
            category=category,
            status=status,
        )

        saved_risk = self.repository.save(risk)

        return RiskDTO.from_entity(saved_risk)
PY

# ------------------------------------------------
# 5. USE CASE - GET RISK
# ------------------------------------------------

cat << 'PY' > application/use_cases/get_risk.py
from application.dto.risk_dto import RiskDTO
from application.services.risk_service import RiskService


class GetRiskUseCase:

    def __init__(self, service: RiskService):
        self.service = service

    def execute(self, code: str) -> RiskDTO | None:
        return self.service.get_risk(code)
PY

# ------------------------------------------------
# 6. USE CASE - LIST RISKS
# ------------------------------------------------

cat << 'PY' > application/use_cases/get_risks.py
from application.dto.risk_dto import RiskDTO
from application.services.risk_service import RiskService


class GetRisksUseCase:

    def __init__(self, service: RiskService):
        self.service = service

    def execute(self) -> list[RiskDTO]:
        return self.service.get_all_risks()
PY

# ------------------------------------------------
# 7. DEPENDENCY INJECTION CONTAINER
# ------------------------------------------------

cat << 'PY' > infrastructure/container/container.py
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
PY

# ------------------------------------------------
# 8. FASTAPI DEPENDENCY PROVIDER
# ------------------------------------------------

cat << 'PY' > presentation/api/dependencies.py
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
PY

# ------------------------------------------------
# 9. CONTROLLER
# ------------------------------------------------

cat << 'PY' > presentation/api/controllers/risk_controller.py
from application.dto.risk_dto import RiskDTO
from application.services.risk_service import RiskService


class RiskController:

    def __init__(self, service: RiskService):
        self.service = service

    def get_all(self) -> list[RiskDTO]:
        return self.service.get_all_risks()

    def get_by_code(self, code: str) -> RiskDTO | None:
        return self.service.get_risk(code)
PY

# ------------------------------------------------
# 10. PRESENTATION SCHEMA
# ------------------------------------------------

cat << 'PY' > presentation/schemas/risk_schema.py
from pydantic import BaseModel


class RiskResponse(BaseModel):
    code: str
    name: str
    description: str | None
    category: str | None
    probability: int
    impact: int
    risk_score: int
    risk_level: str
    status: str | None

    model_config = {
        "from_attributes": True
    }
PY

# ------------------------------------------------
# 11. NEW MODULAR ROUTES
# ------------------------------------------------

cat << 'PY' > presentation/api/routes/risk_routes.py
from fastapi import APIRouter, Depends, HTTPException

from application.services.risk_service import RiskService
from application.use_cases.get_risk import GetRiskUseCase
from application.use_cases.get_risks import GetRisksUseCase

from presentation.api.dependencies import get_risk_service
from presentation.schemas.risk_schema import RiskResponse


router = APIRouter(
    prefix="/api/v2/risks",
    tags=["Risk Management - OOP"]
)


@router.get(
    "",
    response_model=list[RiskResponse]
)
def get_risks(
    service: RiskService = Depends(get_risk_service),
):
    use_case = GetRisksUseCase(service)

    return use_case.execute()


@router.get(
    "/{code}",
    response_model=RiskResponse
)
def get_risk(
    code: str,
    service: RiskService = Depends(get_risk_service),
):
    use_case = GetRiskUseCase(service)

    risk = use_case.execute(code)

    if risk is None:
        raise HTTPException(
            status_code=404,
            detail=f"Risk {code} not found"
        )

    return risk
PY

# ------------------------------------------------
# 12. ROUTES PACKAGE
# ------------------------------------------------

cat << 'PY' > presentation/api/routes/__init__.py
from presentation.api.routes.risk_routes import router as risk_router

__all__ = [
    "risk_router",
]
PY

# ------------------------------------------------
# 13. PRESENTATION DEPENDENCIES PACKAGE
# ------------------------------------------------

touch presentation/api/dependencies.py

# ------------------------------------------------
# 14. TESTS FOR REPOSITORY / SERVICE / DTO
# ------------------------------------------------

mkdir -p tests/unit

cat << 'PY' > tests/unit/test_risk_dto.py
from application.dto.risk_dto import RiskDTO
from domain.entities.risk import Risk


def test_risk_dto_from_entity():
    risk = Risk(
        code="RISK-TEST",
        name="Test Risk",
        probability=4,
        impact=5,
        description="Test",
        category="Electrical",
        status="active",
    )

    dto = RiskDTO.from_entity(risk)

    assert dto.code == "RISK-TEST"
    assert dto.risk_score == 20
    assert dto.risk_level == "Critical"
PY

cat << 'PY' > tests/unit/test_risk_service.py
from application.services.risk_service import RiskService
from domain.entities.risk import Risk


class FakeRiskRepository:

    def __init__(self):
        self.risks = [
            Risk(
                code="RISK-001",
                name="Electrical contact",
                probability=4,
                impact=5,
            )
        ]

    def find_by_id(self, risk_id):
        return None

    def find_by_code(self, code):
        for risk in self.risks:
            if risk.code == code:
                return risk

        return None

    def find_all(self):
        return self.risks

    def save(self, risk):
        self.risks.append(risk)
        return risk


def test_risk_service_get_risk():
    service = RiskService(FakeRiskRepository())

    result = service.get_risk("RISK-001")

    assert result is not None
    assert result.code == "RISK-001"
    assert result.risk_score == 20


def test_risk_service_get_all():
    service = RiskService(FakeRiskRepository())

    result = service.get_all_risks()

    assert len(result) == 1
    assert result[0].code == "RISK-001"
PY

# ------------------------------------------------
# 15. COMPILE CHECK
# ------------------------------------------------

echo ""
echo "Checking Python compilation..."

python -m compileall \
    domain \
    application \
    infrastructure \
    presentation

# ------------------------------------------------
# 16. UNIT TESTS
# ------------------------------------------------

echo ""
echo "Running unit tests..."

python -m pytest tests/unit -v

echo ""
echo "=============================================="
echo "PHASE B CREATED SUCCESSFULLY"
echo "=============================================="

echo ""
echo "Existing database preserved:"
echo "  data/riskguard.db"
echo ""

echo "Existing semantic files preserved:"
echo "  data/riskguard.ttl"
echo "  semantic/ontology.ttl"
echo ""

echo "New OOP API:"
echo "  GET /api/v2/risks"
echo "  GET /api/v2/risks/RISK-001"
echo ""

echo "Architecture:"
echo "  FastAPI"
echo "      -> Dependency Injection"
echo "      -> Controller"
echo "      -> Use Case"
echo "      -> Service"
echo "      -> Repository Interface"
echo "      -> SQL Repository"
echo "      -> SQLAlchemy"
echo "      -> SQLite"
echo ""
