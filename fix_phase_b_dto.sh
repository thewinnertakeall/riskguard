#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

echo "=============================================="
echo "RISKGUARD - FIX PHASE B DTO"
echo "Value Objects -> DTO primitives"
echo "=============================================="

cat << 'PY' > application/dto/risk_dto.py
from dataclasses import dataclass


@dataclass
class RiskDTO:
    """
    Data Transfer Object used at the application/presentation boundary.

    Domain Value Objects are converted to primitive values here so that
    external layers do not depend on domain implementation details.
    """

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
        score = risk.calculate_score()
        level = risk.classify()

        # Convert RiskScore Value Object to int.
        if hasattr(score, "value"):
            score = score.value

        # Convert RiskLevel Enum / Value Object to string.
        if hasattr(level, "value"):
            level = level.value
        else:
            level = str(level)

        return cls(
            code=risk.code,
            name=risk.name,
            description=risk.description,
            category=risk.category,
            probability=risk.probability,
            impact=risk.impact,
            risk_score=int(score),
            risk_level=str(level),
            status=risk.status,
        )
PY

echo ""
echo "Running DTO and service tests..."

python -m pytest \
    tests/unit/test_risk_dto.py \
    tests/unit/test_risk_service.py \
    -v

echo ""
echo "Running complete unit test suite..."

python -m pytest tests/unit -v

echo ""
echo "Checking compilation..."

python -m compileall \
    domain \
    application \
    infrastructure \
    presentation

echo ""
echo "=============================================="
echo "DTO FIX COMPLETED"
echo "=============================================="
