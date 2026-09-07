from application.dto.risk_dto import RiskDTO
from application.services.risk_service import RiskService


class GetRiskUseCase:

    def __init__(self, service: RiskService):
        self.service = service

    def execute(self, code: str) -> RiskDTO | None:
        return self.service.get_risk(code)
