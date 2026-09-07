from sqlalchemy.orm import Session

from application.services.risk_iso_service import RiskISOService


class DeleteRiskISOControlUseCase:

    def execute(
        self,
        db: Session,
        risk_code: str,
        iso_control_code: str,
    ):
        return RiskISOService.delete_link(
            db=db,
            risk_code=risk_code,
            iso_control_code=iso_control_code,
        )
