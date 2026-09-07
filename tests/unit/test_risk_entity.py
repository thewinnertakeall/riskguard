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
