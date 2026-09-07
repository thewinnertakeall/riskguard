"""
RF-07 - API de análisis de datos públicos.

Responsabilidad:
    Exponer los resultados del servicio RF-07.

No contiene lógica de análisis.
No modifica la base de datos.
No modifica controles.
"""

from fastapi import APIRouter

from scripts.rf07.service import PublicRiskAnalysisService


router = APIRouter(
    prefix="/api/rf07",
    tags=["RF-07 - Public Risk Analysis"],
)

service = PublicRiskAnalysisService()


@router.get("/analysis")
def get_public_risk_analysis():
    """
    Devuelve el análisis completo de los datos públicos
    previamente cargados por RF-06.
    """
    return service.get_analysis()
