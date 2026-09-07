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
