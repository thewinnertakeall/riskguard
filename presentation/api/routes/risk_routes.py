from fastapi import APIRouter, Depends, HTTPException

from application.services.risk_service import RiskService
from application.use_cases.get_risk import GetRiskUseCase
from application.use_cases.get_risks import GetRisksUseCase

from presentation.api.dependencies import get_risk_service
from presentation.schemas.risk_schema import RiskResponse


router = APIRouter(
    prefix="/api/v2/risks",
    tags=["Risk Management - OOP"]
)


@router.get(
    "",
    response_model=list[RiskResponse]
)
def get_risks(
    service: RiskService = Depends(get_risk_service),
):
    use_case = GetRisksUseCase(service)

    return use_case.execute()


@router.get(
    "/{code}",
    response_model=RiskResponse
)
def get_risk(
    code: str,
    service: RiskService = Depends(get_risk_service),
):
    use_case = GetRiskUseCase(service)

    risk = use_case.execute(code)

    if risk is None:
        raise HTTPException(
            status_code=404,
            detail=f"Risk {code} not found"
        )

    return risk
