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
