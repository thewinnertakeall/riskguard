#!/bin/bash

set -e

PROJECT_ROOT="$(pwd)"

echo "============================================================"
echo " RISKGUARD - OOP / CLEAN ARCHITECTURE SETUP"
echo "============================================================"
echo "Project: $PROJECT_ROOT"
echo ""

# ============================================================
# CREATE DIRECTORIES
# ============================================================

echo "[1/8] Creating architecture directories..."

mkdir -p domain/entities
mkdir -p domain/value_objects
mkdir -p domain/events
mkdir -p domain/interfaces

mkdir -p application/dto
mkdir -p application/services
mkdir -p application/use_cases

mkdir -p infrastructure/database/models
mkdir -p infrastructure/database/repositories
mkdir -p infrastructure/semantic
mkdir -p infrastructure/events

mkdir -p presentation/api/routes
mkdir -p presentation/api/controllers
mkdir -p presentation/schemas

mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/acceptance

mkdir -p frontend

# ============================================================
# PYTHON INIT FILES
# ============================================================

echo "[2/8] Creating Python packages..."

find domain application infrastructure presentation -type d \
    -exec touch {}/__init__.py \;

touch tests/__init__.py

# ============================================================
# DOMAIN ENTITIES
# ============================================================

echo "[3/8] Creating domain entities..."

cat << 'PY' > domain/entities/base_entity.py
from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseEntity(ABC):
    """
    Base entity for RiskGuard domain objects.
    """

    id: Optional[int] = None
PY


cat << 'PY' > domain/entities/risk.py
from dataclasses import dataclass, field
from typing import Optional

from domain.entities.base_entity import BaseEntity
from domain.value_objects.risk_level import RiskLevel
from domain.value_objects.risk_score import RiskScore


@dataclass
class Risk(BaseEntity):
    """
    Domain entity representing an occupational risk.
    """

    code: str = ""
    name: str = ""
    description: str = ""

    probability: int = 1
    impact: int = 1

    category: str = ""
    status: str = "Active"

    risk_score: Optional[int] = field(default=None)
    risk_level: Optional[str] = field(default=None)

    def calculate_score(self) -> RiskScore:
        score = self.probability * self.impact
        self.risk_score = score
        return RiskScore(score)

    def classify(self) -> RiskLevel:
        if self.risk_score is None:
            self.calculate_score()

        level = RiskLevel.from_score(self.risk_score)
        self.risk_level = level.value

        return level

    def evaluate(self) -> str:
        self.calculate_score()
        return self.classify().value

    def is_critical(self) -> bool:
        if self.risk_score is None:
            self.calculate_score()

        return self.risk_score >= 17
PY


cat << 'PY' > domain/entities/control.py
from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Control(BaseEntity):
    """
    Domain entity representing a risk control.
    """

    code: str = ""
    name: str = ""
    description: str = ""

    control_type: str = ""
    hierarchy_level: str = ""

    effectiveness: float = 0.0
    status: str = "Active"

    def is_effective(self) -> bool:
        return self.effectiveness >= 80.0
PY


cat << 'PY' > domain/entities/incident.py
from dataclasses import dataclass
from datetime import date
from typing import Optional

from domain.entities.base_entity import BaseEntity


@dataclass
class Incident(BaseEntity):
    """
    Domain entity representing an occupational incident.
    """

    code: str = ""
    title: str = ""
    description: str = ""

    incident_date: Optional[date] = None
    incident_type: str = ""
    severity: str = ""
    status: str = "Open"

    def is_high_severity(self) -> bool:
        return self.severity.lower() == "high"

    def is_open(self) -> bool:
        return self.status.lower() == "open"
PY


cat << 'PY' > domain/entities/cause.py
from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Cause(BaseEntity):
    """
    Domain entity representing a risk cause.
    """

    code: str = ""
    name: str = ""
    description: str = ""

    cause_type: str = ""
    status: str = "Active"
PY


cat << 'PY' > domain/entities/process.py
from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Process(BaseEntity):
    """
    Domain entity representing an organizational process.
    """

    code: str = ""
    name: str = ""
    description: str = ""
    status: str = "Active"
PY


cat << 'PY' > domain/entities/area.py
from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Area(BaseEntity):
    """
    Domain entity representing an organizational area.
    """

    code: str = ""
    name: str = ""
    description: str = ""
    status: str = "Active"
PY


cat << 'PY' > domain/entities/location.py
from dataclasses import dataclass

from domain.entities.base_entity import BaseEntity


@dataclass
class Location(BaseEntity):
    """
    Domain entity representing a physical location.
    """

    code: str = ""
    name: str = ""
    description: str = ""
    status: str = "Active"
PY

# ============================================================
# VALUE OBJECTS
# ============================================================

echo "[4/8] Creating value objects..."

cat << 'PY' > domain/value_objects/risk_score.py
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskScore:
    """
    Immutable value object representing a risk score.
    """

    value: int

    def __post_init__(self):
        if not 1 <= self.value <= 25:
            raise ValueError("Risk score must be between 1 and 25.")

    @property
    def is_critical(self) -> bool:
        return self.value >= 17
PY


cat << 'PY' > domain/value_objects/risk_level.py
from enum import Enum


class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

    @classmethod
    def from_score(cls, score: int):
        if score <= 4:
            return cls.LOW

        if score <= 9:
            return cls.MEDIUM

        if score <= 16:
            return cls.HIGH

        return cls.CRITICAL
PY


cat << 'PY' > domain/value_objects/risk_code.py
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskCode:
    """
    Immutable value object for risk identifiers.
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Risk code cannot be empty.")

        if not self.value.startswith("RISK-"):
            raise ValueError(
                "Risk code must follow the RISK-XXX format."
            )
PY

# ============================================================
# DOMAIN INTERFACES / PORTS
# ============================================================

cat << 'PY' > domain/interfaces/risk_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List

from domain.entities.risk import Risk


class RiskRepository(ABC):

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Risk]:
        pass

    @abstractmethod
    def find_all(self) -> List[Risk]:
        pass

    @abstractmethod
    def save(self, risk: Risk) -> Risk:
        pass
PY


cat << 'PY' > domain/interfaces/semantic_repository.py
from abc import ABC, abstractmethod
from typing import Any


class SemanticRepository(ABC):

    @abstractmethod
    def find_risk(self, code: str) -> Any:
        pass

    @abstractmethod
    def find_critical_risks(self) -> Any:
        pass

    @abstractmethod
    def get_graph_status(self) -> dict:
        pass
PY


cat << 'PY' > domain/interfaces/agent.py
from abc import ABC, abstractmethod


class Agent(ABC):
    """
    Base interface for polymorphic RiskGuard agents.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def analyze(self, context: dict) -> dict:
        pass
PY

# ============================================================
# EVENTS
# ============================================================

cat << 'PY' > domain/events/base_event.py
from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DomainEvent(ABC):
    occurred_at: datetime
PY


cat << 'PY' > domain/events/risk_created.py
from dataclasses import dataclass
from datetime import datetime

from domain.events.base_event import DomainEvent


@dataclass
class RiskCreatedEvent(DomainEvent):
    risk_code: str = ""
PY


cat << 'PY' > domain/events/risk_updated.py
from dataclasses import dataclass
from datetime import datetime

from domain.events.base_event import DomainEvent


@dataclass
class RiskUpdatedEvent(DomainEvent):
    risk_code: str = ""
PY

# ============================================================
# DTO
# ============================================================

cat << 'PY' > application/dto/risk_dto.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class RiskDTO:
    """
    Data Transfer Object for Risk.
    """

    code: str
    name: str
    description: str

    probability: int
    impact: int

    risk_score: Optional[int]
    risk_level: Optional[str]

    category: str
    status: str
PY


cat << 'PY' > application/dto/analysis_dto.py
from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class AgentAnalysisDTO:
    """
    DTO representing the result of an agent analysis.
    """

    risk_code: str
    priority: str
    critical: bool

    control_gap: bool = False
    incident_gap: bool = False

    recommendations: List[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)
PY


cat << 'PY' > application/dto/recommendation_dto.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class RecommendationDTO:

    risk_code: str

    priority: str

    recommendations: List[str] = field(
        default_factory=list
    )

    justification: str = ""
PY

# ============================================================
# STRATEGY PATTERN
# ============================================================

cat << 'PY' > application/services/risk_classification_strategy.py
from abc import ABC, abstractmethod

from domain.value_objects.risk_level import RiskLevel


class RiskClassificationStrategy(ABC):

    @abstractmethod
    def classify(self, score: int) -> RiskLevel:
        pass


class StandardRiskClassificationStrategy(
    RiskClassificationStrategy
):
    """
    Standard RiskGuard classification strategy.
    """

    def classify(self, score: int) -> RiskLevel:

        return RiskLevel.from_score(score)
PY

# ============================================================
# REPOSITORY IMPLEMENTATION
# ============================================================

cat << 'PY' > infrastructure/database/repositories/sql_risk_repository.py
from typing import Optional, List

from domain.entities.risk import Risk
from domain.interfaces.risk_repository import RiskRepository


class SQLRiskRepository(RiskRepository):
    """
    SQL repository adapter.

    This class is intentionally separated from the domain.
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def find_by_code(self, code: str) -> Optional[Risk]:

        from app.models import Risk as RiskModel

        session = self.session_factory()

        try:
            model = (
                session.query(RiskModel)
                .filter(RiskModel.code == code)
                .first()
            )

            if model is None:
                return None

            return Risk(
                id=model.id,
                code=model.code,
                name=model.name,
                description=model.description or "",
                probability=model.probability,
                impact=model.impact,
                category=model.category or "",
                status=model.status or "",
                risk_score=model.risk_score,
                risk_level=model.risk_level,
            )

        finally:
            session.close()

    def find_all(self) -> List[Risk]:

        from app.models import Risk as RiskModel

        session = self.session_factory()

        try:
            models = session.query(RiskModel).all()

            return [
                Risk(
                    id=model.id,
                    code=model.code,
                    name=model.name,
                    description=model.description or "",
                    probability=model.probability,
                    impact=model.impact,
                    category=model.category or "",
                    status=model.status or "",
                    risk_score=model.risk_score,
                    risk_level=model.risk_level,
                )
                for model in models
            ]

        finally:
            session.close()

    def save(self, risk: Risk) -> Risk:
        raise NotImplementedError(
            "Create/update persistence will be implemented "
            "through the application use cases."
        )
PY

# ============================================================
# SEMANTIC ADAPTER
# ============================================================

cat << 'PY' > infrastructure/semantic/rdf_semantic_repository.py
from pathlib import Path

from rdflib import Graph

from domain.interfaces.semantic_repository import (
    SemanticRepository
)


class RDFSemanticRepository(SemanticRepository):
    """
    Adapter between the domain and the RDF knowledge graph.
    """

    def __init__(self, rdf_file=None):

        self.rdf_file = Path(
            rdf_file or "data/riskguard.ttl"
        )

    def _load_graph(self):

        graph = Graph()

        if self.rdf_file.exists():
            graph.parse(
                str(self.rdf_file),
                format="turtle"
            )

        return graph

    def find_risk(self, code: str):

        graph = self._load_graph()

        query = """
        PREFIX rg: <http://riskguard.org/ontology#>

        SELECT ?risk ?name ?score ?level
        WHERE {
            ?risk a rg:Risk ;
                  rg:code ?code ;
                  rg:name ?name ;
                  rg:riskScore ?score ;
                  rg:riskLevel ?level .

            FILTER(?code = ?target)
        }
        """

        return list(
            graph.query(
                query,
                initBindings={"target": code}
            )
        )

    def find_critical_risks(self):

        graph = self._load_graph()

        query = """
        PREFIX rg: <http://riskguard.org/ontology#>

        SELECT ?risk ?code ?name ?score
        WHERE {
            ?risk a rg:Risk ;
                  rg:code ?code ;
                  rg:name ?name ;
                  rg:riskScore ?score .

            FILTER(?score >= 17)
        }
        """

        return list(graph.query(query))

    def get_graph_status(self):

        if not self.rdf_file.exists():

            return {
                "status": "missing",
                "triples": 0,
                "file": str(self.rdf_file)
            }

        graph = self._load_graph()

        return {
            "status": "available",
            "triples": len(graph),
            "file": str(self.rdf_file)
        }
PY

# ============================================================
# EVENT BUS
# ============================================================

cat << 'PY' > infrastructure/events/event_bus.py
from collections import defaultdict
from typing import Callable, Type


class EventBus:
    """
    Lightweight in-process event bus.

    RabbitMQ can replace this adapter later without
    changing domain logic.
    """

    def __init__(self):

        self._handlers = defaultdict(list)

    def subscribe(
        self,
        event_type: Type,
        handler: Callable
    ):

        self._handlers[event_type].append(handler)

    def publish(self, event):

        event_type = type(event)

        for handler in self._handlers[event_type]:
            handler(event)
PY

# ============================================================
# APPLICATION SERVICES
# ============================================================

cat << 'PY' > application/services/risk_service.py
from application.dto.risk_dto import RiskDTO
from application.services.risk_classification_strategy import (
    RiskClassificationStrategy
)


class RiskService:

    def __init__(
        self,
        repository,
        classification_strategy: RiskClassificationStrategy
    ):

        self.repository = repository
        self.classification_strategy = (
            classification_strategy
        )

    def get_risk(self, code: str):

        risk = self.repository.find_by_code(code)

        if risk is None:
            return None

        if risk.risk_score is None:
            risk.calculate_score()

        if risk.risk_level is None:
            risk.risk_level = (
                self.classification_strategy
                .classify(risk.risk_score)
                .value
            )

        return RiskDTO(
            code=risk.code,
            name=risk.name,
            description=risk.description,
            probability=risk.probability,
            impact=risk.impact,
            risk_score=risk.risk_score,
            risk_level=risk.risk_level,
            category=risk.category,
            status=risk.status,
        )

    def get_all_risks(self):

        risks = self.repository.find_all()

        result = []

        for risk in risks:

            if risk.risk_score is None:
                risk.calculate_score()

            if risk.risk_level is None:
                risk.risk_level = (
                    self.classification_strategy
                    .classify(risk.risk_score)
                    .value
                )

            result.append(
                RiskDTO(
                    code=risk.code,
                    name=risk.name,
                    description=risk.description,
                    probability=risk.probability,
                    impact=risk.impact,
                    risk_score=risk.risk_score,
                    risk_level=risk.risk_level,
                    category=risk.category,
                    status=risk.status,
                )
            )

        return result
PY


cat << 'PY' > application/services/semantic_service.py
class SemanticService:

    def __init__(self, semantic_repository):
        self.semantic_repository = semantic_repository

    def get_status(self):
        return self.semantic_repository.get_graph_status()

    def get_risk(self, code: str):
        return self.semantic_repository.find_risk(code)

    def get_critical_risks(self):
        return (
            self.semantic_repository
            .find_critical_risks()
        )
PY

# ============================================================
# USE CASES
# ============================================================

cat << 'PY' > application/use_cases/analyze_risk.py
class AnalyzeRiskUseCase:
    """
    Application use case for risk analysis.
    """

    def __init__(self, coordinator):
        self.coordinator = coordinator

    def execute(self, risk_code: str):

        return self.coordinator.analyze(risk_code)
PY


cat << 'PY' > application/use_cases/synchronize_graph.py
class SynchronizeGraphUseCase:

    def __init__(self, synchronization_service):
        self.synchronization_service = (
            synchronization_service
        )

    def execute(self):

        return (
            self.synchronization_service
            .synchronize()
        )
PY


cat << 'PY' > application/use_cases/get_risk_dashboard.py
class GetRiskDashboardUseCase:
    """
    Aggregates the information required by the dashboard.
    """

    def __init__(
        self,
        risk_service,
        semantic_service,
        coordinator
    ):

        self.risk_service = risk_service
        self.semantic_service = semantic_service
        self.coordinator = coordinator

    def execute(self, risk_code: str):

        risk = self.risk_service.get_risk(
            risk_code
        )

        semantic = self.semantic_service.get_status()

        analysis = self.coordinator.analyze(
            risk_code
        )

        return {
            "risk": risk,
            "semantic": semantic,
            "analysis": analysis,
        }
PY

# ============================================================
# AGENT BASE + FACTORY
# ============================================================

echo "[5/8] Creating polymorphic agent architecture..."

cat << 'PY' > agents/base_agent.py
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all RiskGuard agents.
    """

    def __init__(self, name: str):

        self._name = name

    @property
    def name(self) -> str:

        return self._name

    @abstractmethod
    def analyze(self, context: dict) -> dict:
        """
        Execute agent analysis.
        """
        pass
PY


cat << 'PY' > agents/agent_factory.py
from agents.risk_analysis_agent import RiskAnalysisAgent
from agents.control_analysis_agent import ControlAnalysisAgent
from agents.incident_analysis_agent import IncidentAnalysisAgent
from agents.recommendation_agent import RecommendationAgent


class AgentFactory:
    """
    Factory responsible for constructing agents.
    """

    @staticmethod
    def create(agent_type: str):

        agents = {
            "risk": RiskAnalysisAgent,
            "control": ControlAnalysisAgent,
            "incident": IncidentAnalysisAgent,
            "recommendation": RecommendationAgent,
        }

        if agent_type not in agents:
            raise ValueError(
                f"Unknown agent type: {agent_type}"
            )

        return agents[agent_type]()
PY

# ============================================================
# PRESENTATION LAYER
# ============================================================

echo "[6/8] Creating presentation layer..."

cat << 'PY' > presentation/api/controllers/risk_controller.py
class RiskController:
    """
    HTTP-independent controller.

    Converts application results into presentation data.
    """

    def __init__(self, risk_service):
        self.risk_service = risk_service

    def get_risks(self):

        return self.risk_service.get_all_risks()

    def get_risk(self, code: str):

        return self.risk_service.get_risk(code)
PY


cat << 'PY' > presentation/schemas/risk_schema.py
from pydantic import BaseModel, ConfigDict


class RiskResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    code: str
    name: str
    description: str

    probability: int
    impact: int

    risk_score: int | None
    risk_level: str | None

    category: str
    status: str
PY

# ============================================================
# FRONTEND PLACEHOLDER
# ============================================================

echo "[7/8] Preparing React frontend..."

cat << 'EOF_FRONT' > frontend/README.md
# RiskGuard Frontend

React + Vite dashboard.

Planned modules:

- Risk dashboard
- Critical risk visualization
- Multi-agent analysis
- Recommendations
- Control gaps
- Incident gaps
- RDF knowledge graph status
- SPARQL / semantic information
EOF_FRONT

# ============================================================
# ARCHITECTURE DOCUMENTATION
# ============================================================

cat << 'EOF_ARCH' > ARCHITECTURE.md
# RiskGuard Architecture

## Architectural Style

RiskGuard follows a modular architecture inspired by:

- Clean Architecture
- Hexagonal Architecture
- Domain-Driven Design
- Object-Oriented Design
- SOLID principles

## Layers

### Domain

Contains:

- Entities
- Value Objects
- Domain Events
- Ports / Interfaces
- Business rules

### Application

Contains:

- DTOs
- Use Cases
- Application Services
- Strategies

### Infrastructure

Contains:

- SQL repositories
- RDF adapters
- Event bus
- Database implementations

### Presentation

Contains:

- Controllers
- API routes
- Request/response schemas

### Agents

Contains:

- Abstract Agent
- Risk Analysis Agent
- Control Analysis Agent
- Incident Analysis Agent
- Recommendation Agent
- Coordinator
- Factory

### Frontend

React + Vite dashboard.

## Main Flow

User
  |
  v
React Dashboard
  |
  v
FastAPI
  |
  v
Controller
  |
  v
DTO
  |
  v
Use Case
  |
  v
Application Service
  |
  +----------------------+
  |                      |
  v                      v
Repository          Semantic Adapter
  |                      |
  v                      v
SQLite               RDF / OWL
                         |
                         v
                       SPARQL
                         |
                         v
                     Reasoning
                         |
                         v
                    Multi-Agent
                         |
                         v
                  Recommendation
                         |
                         v
                    Dashboard

## Design Patterns

- Repository Pattern
- Factory Pattern
- Strategy Pattern
- Adapter Pattern
- Dependency Injection
- Event-driven design
- DTO Pattern

## Important Principle

The domain must not depend directly on:

- FastAPI
- SQLAlchemy
- SQLite
- RDFLib
- React
- RabbitMQ

Infrastructure depends on domain interfaces.

This keeps the system replaceable and extensible.
EOF_ARCH

# ============================================================
# TESTS
# ============================================================

cat << 'PY' > tests/unit/test_risk_entity.py
from domain.entities.risk import Risk


def test_risk_classification():

    risk = Risk(
        code="RISK-001",
        name="Electrical contact",
        probability=4,
        impact=5
    )

    assert risk.calculate_score().value == 20
    assert risk.evaluate() == "Critical"
    assert risk.is_critical() is True
PY


cat << 'PY' > tests/unit/test_risk_strategy.py
from application.services.risk_classification_strategy import (
    StandardRiskClassificationStrategy
)


def test_standard_strategy():

    strategy = StandardRiskClassificationStrategy()

    assert strategy.classify(4).value == "Low"
    assert strategy.classify(9).value == "Medium"
    assert strategy.classify(16).value == "High"
    assert strategy.classify(20).value == "Critical"
PY


# ============================================================
# ARCHITECTURE TREE
# ============================================================

echo "[8/8] Generating architecture report..."

cat << 'EOF_REPORT'

============================================================
 RISKGUARD OOP ARCHITECTURE CREATED
============================================================

DOMAIN
  ├── entities
  ├── value_objects
  ├── events
  └── interfaces

APPLICATION
  ├── dto
  ├── services
  └── use_cases

INFRASTRUCTURE
  ├── database
  ├── semantic
  └── events

PRESENTATION
  ├── api
  └── schemas

AGENTS
  ├── BaseAgent
  ├── AgentFactory
  ├── RiskAnalysisAgent
  ├── ControlAnalysisAgent
  ├── IncidentAnalysisAgent
  ├── RecommendationAgent
  └── CoordinatorAgent

FRONTEND
  └── React + Vite preparation

TESTS
  ├── unit
  ├── integration
  └── acceptance

============================================================
 EXISTING DATA WAS NOT DELETED
============================================================

SQLite:
    data/riskguard.db

RDF:
    data/riskguard.ttl

OWL:
    semantic/ontology.ttl

Existing agents:
    agents/

============================================================
 NEXT STEP
============================================================

Run:

    python -m pytest tests/unit -v

Then:

    find domain application infrastructure presentation agents tests \
        -maxdepth 3 -type f | sort

============================================================

EOF_REPORT

echo "Architecture setup completed."
