from sqlalchemy.orm import Session

from application.services.risk_iso_service import RiskISOService


class GetRiskISOControlsUseCase:

    def execute(
        self,
        db: Session,
        risk_code: str
    ):
        risk, links = RiskISOService.get_links(
            db,
            risk_code
        )

        return risk, links
