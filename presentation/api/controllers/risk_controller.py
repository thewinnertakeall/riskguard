from application.dto.risk_dto import RiskDTO
from application.services.risk_service import RiskService


class RiskController:

    def __init__(self, service: RiskService):
        self.service = service

    def get_all(self) -> list[RiskDTO]:
        return self.service.get_all_risks()

    def get_by_code(self, code: str) -> RiskDTO | None:
        return self.service.get_risk(code)
