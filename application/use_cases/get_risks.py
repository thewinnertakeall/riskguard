from application.dto.risk_dto import RiskDTO
from application.services.risk_service import RiskService


class GetRisksUseCase:

    def __init__(self, service: RiskService):
        self.service = service

    def execute(self) -> list[RiskDTO]:
        return self.service.get_all_risks()
