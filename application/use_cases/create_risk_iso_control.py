from sqlalchemy.orm import Session

from application.services.risk_iso_service import RiskISOService


class CreateRiskISOControlUseCase:

    def execute(
        self,
        db: Session,
        risk_code: str,
        iso_control_code: str,
        treatment_status: str = "Planned",
        notes: str | None = None,
    ):
        return RiskISOService.create_link(
            db=db,
            risk_code=risk_code,
            iso_control_code=iso_control_code,
            treatment_status=treatment_status,
            notes=notes,
        )
