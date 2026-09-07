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
