"""
RF-07 - Servicio de análisis de datos públicos.

Responsabilidad:
    Orquestar repository + módulos de análisis.

No modifica la base de datos.
No modifica controles.
No realiza HTTP.
"""


from scripts.rf07.repository import PublicRiskRepository
from scripts.rf07.analysis.summary import build_summary
from scripts.rf07.analysis.municipality import group_by_municipality
from scripts.rf07.analysis.activity import group_by_activity
from scripts.rf07.analysis.trends import group_by_period
from scripts.rf07.analysis.indicators import build_indicators


class PublicRiskAnalysisService:
    """
    Servicio principal de RF-07.
    """

    def __init__(self, repository=None):
        self.repository = repository or PublicRiskRepository()

    def get_analysis(self):
        records = self.repository.get_all()

        return {
            "summary": build_summary(records),
            "indicators": build_indicators(records),
            "municipalities": group_by_municipality(records),
            "activities": group_by_activity(records),
            "trends": group_by_period(records),
        }
